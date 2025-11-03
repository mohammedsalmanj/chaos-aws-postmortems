# ⚙️ Module 2 — EC2 Chaos: Instance Termination + Disk Fill

## 🎯 Objective
Learn how compute-layer failures impact your system.  
Test monitoring, autoscaling, and recovery for EC2-like events.

---

## 🧩 Local Chaos (Docker)

### Start baseline

docker-compose up -d
curl http://localhost:8080/health


Terminate backend
docker stop backend
curl http://localhost:8080/checkout

Disk-fill test
./stress_disk.sh
curl http://localhost:8080/checkout

Recover
./recover.sh

☁️ AWS FIS Chaos
Termination experiment
aws fis start-experiment \
  --experiment-template-id <terminate-template-id>

Disk-fill experiment
aws fis start-experiment \
  --experiment-template-id <diskfill-template-id>


Check CloudWatch alarms:

StatusCheckFailed_Instance

DiskUsedPercent

🧠 Lessons

Termination drills validate autoscaling.

Disk-fill shows alert & cleanup readiness.

Always tag chaos targets (ChaosTarget=true).

Keep runbooks executable and verified.