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

# Build
docker build -t sandeshs/fraud-api:v1 -f Dockerfile.api .

# Push
docker push sandeshs/fraud-api:v1


# Build
docker build -t sandeshs/dashboard:v1 -f Dockerfile.dashboard .

# Push
docker push sandeshs/dashboard:v1








# Create namespace on both clusters
kubectl --context=cluster-a create namespace fraud-detection
kubectl --context=cluster-b create namespace fraud-detection

# Deploy the Fraud API to both regions
kubectl --context=cluster-a apply -f mainfest/fraud-api-deployment.yaml
kubectl --context=cluster-b apply -f mainfest/fraud-api-deployment.yaml

# Verify the rollout status
kubectl --context=cluster-a get pods -n fraud-detection
kubectl --context=cluster-b get pods -n fraud-detection





gcloud services enable `
    multiclusterservicediscovery.googleapis.com `
    gkehub.googleapis.com `
    trafficdirector.googleapis.com


worload ideneti 
gcloud container clusters update cluster-1 `
    --region=asia-east1 `
    --workload-pool=project-d1a95002-78b0-493b-b7e.svc.id.goog


gcloud container node-pools update default-pool `
    --cluster=cluster-1 `
    --region=asia-east1 `
    --workload-metadata=GKE_METADATA

fleet registration: 

    gcloud container fleet memberships register cluster-a-link `
    --gke-cluster=asia-east1/cluster-1 `
    --enable-workload-identity `
    --project=project-d1a95002-78b0-493b-b7e

gcloud alpha container fleet multi-cluster-services enable

mcs for project fleet 

gcloud container fleet multi-cluster-services enable `
    --project=project-d1a95002-78b0-493b-b7e

gcloud projects add-iam-policy-binding project-d1a95002-78b0-493b-b7e `
    --member="serviceAccount:project-d1a95002-78b0-493b-b7e.svc.id.goog[gke-mcs/gke-mcs-importer]" `
    --role="roles/compute.networkViewer"


kubectl --context=cluster-a apply -f mainfest\service-export.yaml



enabling standard gateway:

gcloud container clusters update cluster-1 `
    --region=asia-east1 `
    --gateway-api=standard `
    --project=project-d1a95002-78b0-493b-b7e

enable the gateway 

gcloud container fleet ingress enable `
    --config-membership=cluster-a-link `
    --project=project-d1a95002-78b0-493b-b7e


    gateway to be applied in main cluster 


    gcloud projects add-iam-policy-binding project-d1a95002-78b0-493b-b7e `
    --member="serviceAccount:service-329313374630@gcp-sa-multiclusteringress.iam.gserviceaccount.com" `
    --role="roles/multiclusteringress.serviceAgent"


    kubectl --context=cluster-a apply -f global-gateway.yaml


    change the svc in yaml file bridge the gap between the GLB to you pod 


we did the forcing 
gcloud compute health-checks update http gkemcg1-fraud-detection-fraud-api-svc-80-y2hbtomeh27v `
    --port=8000 --request-path=/health --global


checking 
 gcloud compute health-checks list --filter="name~fraud-api" --format="table(name, httpHealthCheck.port, httpHealthCheck.requestPath)"



kubectl --context=cluster-a get gateway -A