🚀 Run the Experiment

Navigate to FIS Console → Experiment Templates

Select your template FIS-Workshop-EC2-DiskFill-Test

Click Start Experiment

Tag it for tracking:

Name = EC2_Task_DiskFill_<MMDDYYYY>-x


Observe:

State → Running

Monitor X-Ray Trace Map for the client node (PetSite frontend)

Watch for changes in latency and request faults

📊 Expected Observations
Metric	Observation	Meaning
X-Ray (Trace Map)	Slight latency on one node, but no client 5xx errors	Traffic rerouted correctly
EC2 Metrics (Affected Instance)	Disk usage ↑ → CPU/network ↓	Instance throttled due to disk fill
EC2 Metrics (Healthy AZ)	CPU/network ↑	Load balanced to healthy nodes
✅ Post-Experiment Recovery

Wait until State → Completed

Verify disk usage returns to normal

Confirm application availability

Review CloudWatch logs for the experiment run

📘 Outcome

The disk fill fault did not impact application availability.
Traffic automatically rerouted to healthy EC2 instances in the other AZ.
This confirms the resilience of the PetSite deployment under localized disk failures.

💡 Key Takeaways
Lesson	Description
Isolated Failures	Well-architected apps tolerate single-AZ compute issues
Health Checks & Autoscaling	AWS Auto Scaling + ALB ensure routing away from unhealthy nodes
Observability Value	X-Ray and CloudWatch metrics make failure impact visible
Chaos Value	Controlled disk-fill tests validate resilience assumptions safely


🚀 Run Template
aws fis create-experiment-template \
  --cli-input-json file://fis-template-ec2-diskfill.json


Then start it:

aws fis start-experiment \
  --experiment-template-id <template_id> \
  --tags Name=EC2_Task_DiskFill_$(date +%Y%m%d-%H%M)