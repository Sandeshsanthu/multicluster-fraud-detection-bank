from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib, json, os
import pandas as pd
import numpy as np

app = FastAPI(title='Fraud Detection API')

# Use environment variable or default path for Docker
MODEL_PATH = os.getenv('MODEL_PATH', 'models/fraud_pipeline.joblib')
THRESHOLD_PATH = 'models/threshold.json'

# Load model and threshold at startup
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

@app.post('/score')
def score_transaction(tx: Transaction):
    # Convert Pydantic model to DataFrame for the pipeline
    df = pd.DataFrame([tx.dict()])
    
    # Get probability of class 1 (Fraud)
    prob = pipeline.predict_proba(df)[0][1]
    
    # FIX: Added the mandatory 'else' clause
    decision = 'BLOCKED' if prob >= THRESHOLD else 'APPROVED'
    
    return {
        'transaction_id': tx.transaction_id,
        'fraud_probability': round(float(prob), 4),
        'decision': decision,
        'threshold_used': THRESHOLD
    }

@app.get('/health')
def health(): 
    return {'status': 'ok'}
