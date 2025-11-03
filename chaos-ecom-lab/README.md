# Local AWS-Outage-Style Chaos Lab — E-commerce (Docker)

Purpose:
- Learn how outages (payment gateway, DB, full service) affect an e-commerce flow.
- Test retries, graceful failures, and recovery procedures locally using Docker.

Contents:
- app.py : simple Flask e-commerce app with /purchase, /return, /orders, /health
- payment_mock.py : simple mock payment gateway (can be toggled to fail via FAIL_MODE)
- Dockerfile / payment.Dockerfile : images for web and payment mock
- docker-compose.yml : defines services (web, payment-mock, redis)
- start.sh / stop.sh : bring up / tear down lab
- scenario_outage_payment.sh : simulate payment gateway outage
- scenario_outage_db.sh : simulate DB outage (removes local volume to mimic data loss)
- scenario_full_outage.sh : stop core services to simulate full outage
- restore.sh : restore normal operation
- requirements.txt : python deps

Quick start:
1. Make sure Docker is installed and running.
2. From the project root:
   chmod +x *.sh
   ./start.sh
3. Validate health:
   curl http://localhost:5000/health
4. Trigger a purchase:
   curl -X POST http://localhost:5000/purchase -H 'Content-Type: application/json' -d '{"item":"book","amount":9.99}'
5. Simulate payment outage:
   ./scenario_outage_payment.sh
   Then issue the same purchase request to see a 502 response from /purchase.
6. Restore:
   ./restore.sh

Notes & ideas to extend:
- Add a reverse proxy (Traefik) and simulate network partition by stopping the proxy.
- Add a separate "search" service and simulate partial outage using network controls (tc/netem) for latency/loss.
- Implement retry logic in the web app to test exponential backoff.
- Use chaos tools like `pumba` for more advanced container-level faults (network, pause, kill).

Safety:
- These scripts act on local Docker only; don't run them on production hosts.
