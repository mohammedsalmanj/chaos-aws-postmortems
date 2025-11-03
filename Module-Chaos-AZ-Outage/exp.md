🚀 Step 5: Run the Experiment

Start the experiment manually from the console or CLI:

aws fis start-experiment \
    --experiment-template-id <your-template-id> \
    --tags Name="us-east-1b AZ Execution 1"


✅ Confirm the experiment state changes to Running.
It runs for about 15 minutes.

During execution:

Keep using the PetSite app

Watch CloudWatch RUM and X-Ray dashboards for real-time impact

🔍 Step 6: Observe and Validate
🔹 CloudWatch Dashboard

Traffic continues through the Load Balancer

Small number of 5xx errors appear temporarily

Latency increases briefly during outage window

🔹 RDS

Writer instance fails over to a healthy AZ

Reader reconnects automatically after failover

🔹 EC2 / EKS / ECS

Lost capacity in the impaired AZ is replaced in healthy AZs by Auto Scaling

🔹 X-Ray

Short latency spike

Drop in request count during outage

Few transient 5xx errors observed

🔹 CloudWatch RUM

Slight dip in Apdex (0.69 / 1.0)

Some client reconnections observed

Overall application still available

📈 Results Summary
Metric	Observation	Outcome
RDS Failover	Writer moved to healthy AZ	✅
Load Balancer	Rerouted traffic successfully	✅
User Impact	Minor latency / reconnect	⚠️ Minimal
Availability	99.8% maintained during event	✅
Hypothesis	Held true – system resilient to zonal outage	✅
💡 Analogy

Think of AWS Regions as a power grid with multiple substations (AZs).
When one substation loses power ⚡,
other substations instantly take over the load.
The city (your app) flickers for a second — but stays lit.

🧠 Lessons Learned
Area	Lesson	Action
Multi-AZ Design	Validated proper failover during AZ outage	Continue testing across all AZs
Observability	CloudWatch dashboards clearly showed impact	Include dashboards in automated reports
User Experience	Minor latency impact detected	Optimize ALB health checks
Resilience Practices	Zonal failure simulated successfully	Add Zonal Shift (Route 53 ARC) for gray failures
🧰 Tools Used
Category	Tool
Chaos Simulation	AWS FIS (Scenario: AZ Availability – Power Interruption)
Observability	CloudWatch, X-Ray, RUM
Database	Amazon RDS (Multi-AZ)
Compute	EC2 / ECS / EKS
Reporting	S3 PDF report via FIS
🧩 Outcome Summary

✅ Application stayed available
✅ Traffic shifted to healthy AZs
✅ RDS failover worked automatically
⚠️ Minor temporary user impact (latency + reconnect)