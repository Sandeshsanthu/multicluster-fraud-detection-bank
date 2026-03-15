from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib, json, os, redis
import pandas as pd
import numpy as np

app = FastAPI(title='Fraud Detection API')

# Connect to Redis
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

MODEL_PATH = os.getenv('MODEL_PATH', 'models/fraud_pipeline.joblib')
THRESHOLD_PATH = 'models/threshold.json'

pipeline = joblib.load(MODEL_PATH)
with open(THRESHOLD_PATH) as f:
    THRESHOLD = json.load(f).get('threshold', 0.5)

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    transaction_type: str
    merchant_category: str
    user_id: int
    hour_of_day: int
    country: str
    ip_risk_score: float
    hour: int
    device_risk_score: float

@app.post('/score')
def score_transaction(tx: Transaction):
    # 1. Check Redis Cache
    cache_key = f"fraud:{tx.transaction_id}"
    try:
        cached = r.get(cache_key)
        if cached:
            return json.loads(cached)
    except redis.ConnectionError:
        pass # Continue to scoring if Redis is unreachable

    # 2. Score the transaction
    df = pd.DataFrame([tx.dict()])
    prob = pipeline.predict_proba(df)[0][1]
    decision = 'BLOCKED' if prob >= THRESHOLD else 'APPROVED'
    
    result = {
        'transaction_id': tx.transaction_id,
        'fraud_probability': round(float(prob), 4),
        'decision': decision,
        'threshold_used': THRESHOLD,
        'source': 'model_score' # Helps you see it's not from cache
    }

    # 3. Store in Redis (Cache for 5 minutes)
    try:
        # We add 'source' as 'cache' for future hits
        cache_result = result.copy()
        cache_result['source'] = 'redis_cache'
        r.setex(cache_key, 300, json.dumps(cache_result))
    except redis.ConnectionError:
        pass

    return result

@app.get('/health')
def health(): 
    return {'status': 'ok'}
