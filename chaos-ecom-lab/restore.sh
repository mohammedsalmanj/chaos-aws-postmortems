#!/usr/bin/env bash
set -e
echo "🔧 Restoring payment mock and web services to normal mode..."

# Stop and remove any manually created payment container
docker stop chaos_ecom_payment 2>/dev/null || true
docker rm chaos_ecom_payment 2>/dev/null || true

# Ensure network exists (sometimes removed during chaos)
docker network inspect chaos-ecom-lab_default >/dev/null 2>&1 || \
  docker network create chaos-ecom-lab_default

# Bring up all official services from docker-compose
docker-compose up -d --build

echo "✅ All services restored. Checking status..."
docker-compose ps
