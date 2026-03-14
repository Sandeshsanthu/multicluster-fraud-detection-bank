# multicluster-fraud-detection-bank
first push
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1


python -m src.score_new_transactions data\raw\synthetic_fraud_dataset.csv --output_csv data\processed\my_scored_results.csv
python -m src.train_model
