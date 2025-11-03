#!/usr/bin/env bash
APP_CONTAINER=$(docker-compose ps -q app)
if [ -z "$APP_CONTAINER" ]; then
  echo "Start docker-compose first: docker-compose up -d"
  exit 1
fi
echo "🔧 Restoring DNS..."
docker exec "$APP_CONTAINER" bash -c "if [ -f /etc/resolv.conf.bak ]; then cp /etc/resolv.conf.bak /etc/resolv.conf; else echo 'Backup not found'; fi"
echo "✅ DNS restored inside app container."
