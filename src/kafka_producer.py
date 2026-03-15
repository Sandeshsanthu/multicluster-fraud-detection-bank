from kafka import KafkaProducer
import json, random, time, uuid, os

producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BROKERS', 'localhost:9092'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    tx = {
        'transaction_id': str(uuid.uuid4()),
        'amount': round(random.uniform(10, 5000), 2),
        'transaction_type': random.choice(['Online', 'POS', 'ATM']),
        'merchant_category': random.choice(['Electronics', 'Grocery', 'Travel']),
        'user_id': random.randint(1000, 9999),
        'hour_of_day': random.randint(0, 23),
        'country': 'India', 'ip_risk_score': 0.01, 'hour': 12, 'device_risk_score': 0.01
    }
    producer.send('transactions', value=tx)
    print(f"Sent: {tx['transaction_id']}")
    time.sleep(1)
