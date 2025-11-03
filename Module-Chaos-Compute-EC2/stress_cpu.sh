#!/bin/bash
echo "[+] Starting CPU stress for 2 minutes..."
docker exec backend bash -c "apt-get update >/dev/null && apt-get install -y stress >/dev/null && stress --cpu 2 --timeout 120"
echo "[✓] CPU stress completed."
