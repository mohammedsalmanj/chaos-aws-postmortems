#!/usr/bin/env bash
set -e
echo "Simulating database outage by removing volume (orders data) from web container."
docker-compose stop web
docker volume rm $(docker volume ls -q | grep chaos_ecom_lab_orders || true) || true
echo "Bringing web back (it will recreate DB)."
docker-compose up -d web
echo "DB outage simulated (old data removed)."
