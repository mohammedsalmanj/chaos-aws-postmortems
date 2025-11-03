Local AWS-Outage-Style Chaos Lab — E-Commerce (Docker)
🎯 Purpose

Practice how common AWS-like failures (payment gateway, database, or full-service outage) affect an e-commerce transaction flow.
Train detection, retry logic, graceful degradation, and quick recovery locally using Docker, before testing in AWS FIS.

🧱 Components
File	Purpose
app.py	Flask web service exposing /purchase, /return, /orders, /health
payment_mock.py	Mock payment gateway; failure toggled via FAIL_MODE env var
Dockerfile, payment.Dockerfile	Build images for web + payment services
docker-compose.yml	Defines stack: web, payment-mock, redis
start.sh, stop.sh	Bring up / tear down the entire lab
scenario_outage_payment.sh	Simulate payment-gateway outage
scenario_outage_db.sh	Simulate DB outage (volume removal)
scenario_full_outage.sh	Kill all core services (complete outage)
restore.sh	Restore normal operations
requirements.txt	Python dependencies
⚙️ Quick Start
# 1️⃣  Clone & enter repo
git clone https://github.com/<yourname>/chaos-aws-postmortems.git
cd chaos-aws-postmortems/module-1-ecom-dns-outage

# 2️⃣  Make scripts executable
chmod +x *.sh

# 3️⃣  Start baseline environment
./start.sh

# 4️⃣  Validate health
curl http://localhost:5000/health
# → {"status":"ok"}

# 5️⃣  Simulate a purchase
curl -X POST http://localhost:5000/purchase \
     -H 'Content-Type: application/json' \
     -d '{"item":"book","amount":9.99}'
# → {"status":"success"}

# 6️⃣  Trigger a payment outage
./scenario_outage_payment.sh

# 7️⃣  Retry the purchase (expect failure)
curl -X POST http://localhost:5000/purchase \
     -H 'Content-Type: application/json' \
     -d '{"item":"book","amount":9.99}'
# → 502 Bad Gateway / {"error":"payment service unavailable"}

# 8️⃣  Restore system
./restore.sh

# 9️⃣  Stop the lab
./stop.sh

🧪 Extra Chaos Scenarios
Script	Description
scenario_outage_payment.sh	Sets FAIL_MODE=1 → mock payment 5xx errors
scenario_outage_db.sh	Removes Redis/Postgres volume → mimics DB corruption
scenario_full_outage.sh	Stops web + payment containers (complete blackout)
restore.sh	Brings all services & volumes back
💥 Advanced Commands (Manual Injection)
# Pause payment container for 30 s
docker pause payment-mock && sleep 30 && docker unpause payment-mock

# Add network latency (Linux only)
sudo tc qdisc add dev docker0 root netem delay 200ms

# Drop all outbound DNS to mimic AWS Route53 failure
docker exec web bash -c "iptables -A OUTPUT -p udp --dport 53 -j DROP"

🔬 Observability Ideas
Tool	What to Watch
Docker logs	Transaction errors, retries
curl timings (-w '%{time_total}')	Measure latency impact
New Relic / OpenTelemetry agent	Trace purchase → payment chain
Grafana / Prometheus (optional)	Request rate, error %, latency 95p
🧠 Learning Goals
Topic	Skill Practiced
Failure Isolation	Identify the root (DNS, DB, payment) quickly
Retry Strategy	Implement exponential backoff in app.py
Observability	Connect logs, traces, and metrics
Recovery Process	Run restore.sh + validate health endpoints
Communication	Write quick postmortem in /postmortems/
💡 Ideas to Extend

Add a reverse proxy (Traefik/Nginx) → simulate network partitions by stopping proxy.

Add a “search” service → apply latency via tc/netem for partial outage.

Integrate chaos tools like pumba or litmus for random container kills.

Create an AWS FIS template mirroring this stack on EC2 for cloud-level validation.

⚠️ Safety Notice

These scripts target local Docker only.
Do not run them on production hosts or shared environments.
Always review any iptables, tc, or docker rm commands before execution.