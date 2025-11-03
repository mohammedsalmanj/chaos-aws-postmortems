#!/bin/bash
echo "[+] Filling disk space in backend container..."
docker exec backend bash -c "fallocate -l 500M /tmp/fillfile && df -h /tmp"
echo "[!] Disk filled. App likely degraded."
echo "Run ./recover.sh to clean up."
