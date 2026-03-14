# src/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib, json, numpy as np
import pandas as pd

app = FastAPI(title='Fraud Detection API')

# Load model and threshold at startup
pipeline = joblib.load('models/fraud_pipeline.joblib')
with open('models/threshold.json') as f:
    THRESHOLD = json.load(f)['threshold']

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    transaction_type: str
    merchant_category: str
    user_id: int
    hour_of_day: int
    # add your other features here

@app.post('/score')
def score_transaction(tx: Transaction):
    df = pd.DataFrame([tx.dict()])
    prob = pipeline.predict_proba(df)[0][1]
    decision = 'BLOCKED' if prob >= THRESHOLD 
    return {
        'transaction_id': tx.transaction_id,
        'fraud_probability': round(float(prob), 4),
        'decision': decision,
        'threshold_used': THRESHOLD
    }

@app.get('/health')
def health(): return {'status': 'ok'}
