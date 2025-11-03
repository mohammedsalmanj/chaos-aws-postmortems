#!/usr/bin/env bash
URL="http://localhost:5000/purchase"
for i in $(seq 1 5); do
  body="{\"user\":\"salman\",\"amount\":$(( (RANDOM % 100) + 1 )), \"item\":\"sku-$i\"}"
  echo "🛒 Posting order $i..."
  http_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$body" "$URL")
  echo "Result HTTP $http_code"
  sleep 1
done
