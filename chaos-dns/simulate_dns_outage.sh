#!/usr/bin/env bash
APP_CONTAINER=$(docker-compose ps -q app)
if [ -z "$APP_CONTAINER" ]; then
  echo "Start docker-compose first: docker-compose up -d"
  exit 1
fi
echo "📉 Simulating DNS outage..."
docker exec "$APP_CONTAINER" bash -c "cp /etc/resolv.conf /etc/resolv.conf.bak || true"
docker exec "$APP_CONTAINER" bash -c "echo '' > /etc/resolv.conf"
echo "✅ DNS outage simulated inside app container."
