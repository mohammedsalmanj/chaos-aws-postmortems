🚀 Run the Experiment
1. Record Baseline State

Open RDS Console → Databases

Review your Aurora Cluster — note:

Writer instance (Region + AZ)

Reader instance (Region + AZ)

2. Start the FIS Experiment

Go to FIS → Experiment Templates

Select your template FisWorkshopRds

Add:

Key: Name

Value: RDS-Reboot-Reader

Click Start Experiment

Confirm execution.

✅ You should see the reader instance rebooting in RDS Console.

🔍 Analyze Results

After the reboot completes:

Check RDS Console:

Reader instance status → “Available” again

Cluster → healthy

Open CloudWatch → X-Ray Trace Map:

Observe traces during reboot window.

Look for spikes in latency or faults.

You should find that:

No significant Faults or 503s occurred.

The reader rejoined seamlessly.

The application continued to serve traffic via the writer instance.

📈 Expected Observations
Metric	Expected Behavior
RDS Reader State	“Rebooting” → “Available”
Aurora Cluster	Healthy (no failover triggered)
Application Errors	None / minimal
X-Ray Faults	No spike detected
Recovery Time	Few minutes
💡 Analogy

Think of Aurora as a team of servers in a restaurant kitchen 👩‍🍳

The Writer instance is the head chef — always working.

The Reader instance is the assistant chef — helps with prep work.

During maintenance, the assistant takes a short break (reboot).
The head chef keeps cooking — customers don’t notice any difference.
When the assistant returns, they rejoin smoothly without disturbing service.

🧠 Key Takeaways
Area	Lesson
Resilience	Aurora automatically maintains availability even during reader reboot.
Observability	Use X-Ray + CloudWatch to confirm no end-user impact.
Fault Injection	FIS safely tests real AWS failure scenarios.
Preparedness	Regularly rehearse DB maintenance events to confirm failover reliability.
🧰 Tools Used

AWS Fault Injection Service (FIS) — fault simulation

Amazon RDS (Aurora) — Multi-AZ cluster

Amazon ECS — load generator service

AWS X-Ray / CloudWatch — observability and fault tracking