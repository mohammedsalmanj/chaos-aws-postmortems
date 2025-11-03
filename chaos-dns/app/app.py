import os
import time
import threading
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from flask import Flask, jsonify, request

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localstack:4566")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "orders-queue")
DDB_TABLE_NAME = os.getenv("DDB_TABLE_NAME", "Orders")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")

# ---------------------------------------------------------------------------
# AWS Session setup (LocalStack-compatible)
# ---------------------------------------------------------------------------
session = boto3.session.Session()

sqs = session.client(
    'sqs',
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=boto3.session.Config(signature_version='v4')
)

dynamodb = session.client(
    'dynamodb',
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

QUEUE_URL = None

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Bootstrap Function
# ---------------------------------------------------------------------------
def bootstrap_resources():
    global QUEUE_URL
    print("🚀 Bootstrapping app...")

    # --- Create SQS Queue ---
    try:
        resp = sqs.create_queue(QueueName=SQS_QUEUE_NAME)
        QUEUE_URL = resp['QueueUrl']
        print(f"✅ SQS queue ready: {QUEUE_URL}")
    except ClientError as e:
        print(f"❌ Error creating SQS queue: {e}")

    # --- Create DynamoDB Table ---
    try:
        existing = dynamodb.list_tables()
        if DDB_TABLE_NAME not in existing['TableNames']:
            dynamodb.create_table(
                TableName=DDB_TABLE_NAME,
                KeySchema=[{"AttributeName": "order_id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "order_id", "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            print("⏳ Creating DynamoDB table, waiting...")
            waiter = dynamodb.get_waiter('table_exists')
            waiter.wait(TableName=DDB_TABLE_NAME)
        print("✅ DynamoDB table created.")
    except ClientError as e:
        print(f"❌ Error creating table: {e}")
    except Exception as e:
        print(f"Could not list tables yet: {e}")

# ---------------------------------------------------------------------------
# SQS Worker Thread
# ---------------------------------------------------------------------------
def worker():
    print("📦 SQS worker started, polling queue...")
    while True:
        try:
            if not QUEUE_URL:
                time.sleep(3)
                continue
            msgs = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=5
            )
            for msg in msgs.get('Messages', []):
                print(f"🧾 Received message: {msg['Body']}")
                order_id = msg['MessageId']
                try:
                    dynamodb.put_item(
                        TableName=DDB_TABLE_NAME,
                        Item={"order_id": {"S": order_id}, "details": {"S": msg['Body']}}
                    )
                    print("✅ Order saved to DynamoDB.")
                except ClientError as e:
                    print(f"❌ DynamoDB write error: {e}")
                sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])
        except EndpointConnectionError:
            print("🌐 Connection issue — retrying...")
            time.sleep(3)
        except ClientError as e:
            print(f"Worker error: {e}")
            time.sleep(2)

# ---------------------------------------------------------------------------
# Flask Routes
# ---------------------------------------------------------------------------
@app.route('/')
def health():
    return jsonify({"status": "ok", "message": "App running"})

@app.route('/order', methods=['POST'])
def place_order():
    try:
        order = request.json
        print(f"🛒 Received order: {order}")

        # Try pushing to SQS
        if QUEUE_URL:
            sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=str(order))
            return jsonify({"status": "queued", "order": order}), 201
        else:
            print("⚠️ Queue not available, returning 202 (accepted).")
            return jsonify({"status": "retry_later", "order": order}), 202
    except Exception as e:
        print(f"❌ Error in /order: {e}")
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    bootstrap_resources()
    threading.Thread(target=worker, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
