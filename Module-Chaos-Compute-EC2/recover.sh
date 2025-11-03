#!/bin/bash
# ────────────────────────────────────────────────
# Chaos AWS Postmortems - Module 2 (EC2 Chaos)
# Recovery Script
# ────────────────────────────────────────────────
# Restores the backend container and clears any simulated stress or disk fill

echo "🧩  Starting recovery process..."

# 1️⃣  Remove any fill files (if disk-fill chaos was run)
if docker ps --format '{{.Names}}' | grep -q backend; then
  echo "🧹  Cleaning temporary fill files from backend..."
  docker exec backend bash -c "rm -f /tmp/fillfile /tmp/fillfile* 2>/dev/null || true"
fi

# 2️⃣  Unpause or restart backend container if stopped
if [ "$(docker ps -a --filter "name=backend" --format "{{.State}}")" != "running" ]; then
  echo "🚀  Restarting backend container..."
  docker start backend >/dev/null 2>&1 || docker restart backend >/dev/null 2>&1
else
  echo "✅  Backend container already running."
fi

# 3️⃣  Verify all core services are up
echo "🔎  Checking container health..."
docker ps --format "table {{.Names}}\t{{.Status}}"

# 4️⃣  Optional: remove chaos iptables rules if any were injected manually
echo "🧱  Checking for local iptables DNS rules (optional cleanup)..."
if docker exec backend bash -c "iptables -S | grep -q 'dport 53'"; then
  docker exec backend bash -c "iptables -F"
  echo "✅  Cleared DNS block rules inside backend."
else
  echo "ℹ️  No DNS rules to clean."
fi

# 5️⃣  Confirm app health endpoint
echo "🩺  Validating service health..."
sleep 3
curl -s http://localhost:8080/health || echo "⚠️  Health endpoint not reachable yet — check logs."

echo "🎉  Recovery complete!"
