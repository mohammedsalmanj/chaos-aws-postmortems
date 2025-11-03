#!/usr/bin/env bash
echo "Simulating payment gateway outage..."

# Stop and remove the existing payment container
docker stop chaos_ecom_payment 2>/dev/null || true
docker rm chaos_ecom_payment 2>/dev/null || true

# Recreate container using the built image, but override FAIL_MODE=1
docker run -d \
  --name chaos_ecom_payment \
  -e FAIL_MODE=1 \
  --network chaos-ecom-lab_default \
  -p 5001:5001 \
  chaos-ecom-lab-payment-mock

echo "Payment mock started in FAIL_MODE=1 (returns 502). Trigger a purchase to observe failure."
