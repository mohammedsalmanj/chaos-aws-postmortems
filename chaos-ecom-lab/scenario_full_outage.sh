#!/usr/bin/env bash
set -e
echo "Simulating full service outage by stopping web and payment containers..."
docker container stop chaos_ecom_web chaos_ecom_payment || true
echo "All core services stopped. Use restore.sh to bring them back."
