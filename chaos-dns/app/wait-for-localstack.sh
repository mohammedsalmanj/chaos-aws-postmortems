#!/usr/bin/env bash
set -e

echo "⏳ Waiting for LocalStack (SQS & DynamoDB) to respond..."

# Loop until both SQS and DynamoDB can be listed successfully
until aws --endpoint-url=http://localstack:4566 sqs list-queues >/dev/null 2>&1 \
  && aws --endpoint-url=http://localstack:4566 dynamodb list-tables >/dev/null 2>&1; do
  sleep 2
  echo "⌛ Still waiting for LocalStack..."
done

echo "✅ LocalStack APIs are responding. Starting Flask app..."
exec python app.py
