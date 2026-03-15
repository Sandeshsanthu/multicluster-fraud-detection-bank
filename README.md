# multicluster-fraud-detection-bank
first push
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1


python -m src.score_new_transactions data\raw\synthetic_fraud_dataset.csv --output_csv data\processed\my_scored_results.csv
python -m src.train_model

sudo docker compose up --build

curl -X POST http://localhost:8000/score   -H 'Content-Type: application/json'   -d '{
    "transaction_id": "T001",
    "amount": 1500,
    "transaction_type": "Online",
    "merchant_category": "Electronics",
    "user_id": 9876,
    "hour_of_day": 2,
    "country": "India",
    "ip_risk_score": 0.1,
    "hour": 2,
    "device_risk_score": 0.05
  }'

Copy-Item Dockerfile.api Dockerfile
gcloud builds submit . --tag="us-central1-docker.pkg.dev/$PROJECT_ID/fraud-repo/fraud-api:v1"
Remove-Item Dockerfile

Copy-Item Dockerfile.dashboard Dockerfile
gcloud builds submit . --tag="us-central1-docker.pkg.dev/$PROJECT_ID/fraud-repo/fraud-dashboard:v1"
Remove-Item Dockerfile
