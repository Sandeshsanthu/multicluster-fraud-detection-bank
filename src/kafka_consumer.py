from kafka import KafkaConsumer
import json, joblib, pandas as pd, logging, redis, os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('fraud-consumer')

# Load model & threshold
pipeline = joblib.load('models/fraud_pipeline.joblib')
with open('models/threshold.json') as f:
    THRESHOLD = json.load(f)['threshold']

# Connect to Kafka & Redis
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=os.getenv('KAFKA_BROKERS', 'kafka-service:9092'),
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='fraud-detection-group'
)
r = redis.Redis(host=os.getenv('REDIS_HOST', '34.118.238.237'), decode_responses=True)

logger.info('Listening for transactions...')
for message in consumer:
    tx = message.value
    try:
        df = pd.DataFrame([tx])
        prob = pipeline.predict_proba(df)[0][1]
        decision = 'BLOCKED' if prob >= THRESHOLD else 'APPROVED'
        
        result = {'transaction_id': tx['transaction_id'], 'fraud_probability': round(float(prob), 4), 'decision': decision}
        r.setex(f"fraud:{tx['transaction_id']}", 300, json.dumps(result))
        logger.info(f"Scored: {tx['transaction_id']} -> {decision}")
    except Exception as e:
        logger.error(f'Error: {e}')
