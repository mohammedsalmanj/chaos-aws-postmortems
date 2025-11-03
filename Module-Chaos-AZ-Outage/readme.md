🎯 Objective

Validate that your multi-AZ architecture can sustain service continuity when one entire Availability Zone (AZ) experiences a simulated power interruption.

Specifically, ensure that:

Traffic automatically shifts to healthy AZs

RDS failover, EC2 Auto Scaling, and Load Balancing behave as expected

End users experience minimal or no interruption

🧠 Experiment Idea

AWS designed each AZ to be an isolated fault domain.
If one AZ loses power or networking, your workloads in other AZs should continue serving traffic.

This chaos experiment simulates such an AZ-level outage using AWS Fault Injection Service (FIS) with the “AZ Availability: Power Interruption” scenario.

Hypothesis:
If one AZ (e.g., us-east-1b) is impaired,

RDS should failover to another AZ automatically

Auto Scaling Groups should replace lost EC2 capacity in healthy AZs

Load Balancers should reroute user requests seamlessly

🧱 Setup Overview
Component	Description
Application	PetSite (multi-tier app with EC2/EKS/ECS + RDS)
Region	us-east-1
Target AZ	us-east-1b
Chaos Tool	AWS Fault Injection Service (Scenario Library)
Scenario	AZ Availability: Power Interruption
IAM Role	fis-az-role
Observability	CloudWatch Dashboard: AvailabilityZonePowerImpairment
⚙️ Step 1: Prepare

Identify where your RDS writer instance is located.

Go to Amazon RDS → Databases → Cluster details

Note the AZ of the writer (e.g., us-east-1b)

That’s the AZ you’ll target in this experiment.

⚙️ Step 2: Create the Experiment Template

Go to AWS FIS → Scenario Library → “AZ Availability: Power Interruption”

Click Create template with scenario

🧩 Shared Parameters
Parameter	Value
affectedAz	us-east-1b
affectedRolesForInsufficientCapacityException	FisServerless-FISDummyRoleForASG... (dummy IAM role)
targetingTags	Key: AzImpairmentPower, Value: Ready
dnsImpactDuration	2m
outageDuration	10m
recoveryDuration	5m

💡 All PetSite components are pre-tagged with AzImpairmentPower=Ready for the experiment.

⚙️ Step 3: Configure Access and Reporting

Service Access: Existing IAM role → fis-az-role

Logs: CloudWatch log group → FISExperiments

Report:

S3 Bucket → services-fisreportbucket

CloudWatch Dashboard → AvailabilityZonePowerImpairment

Pre-experiment duration: 10 min

Post-experiment duration: 5 min

Enable Include CloudWatch Metrics ✅

🧪 Step 4: Target Preview (Optional but Recommended)

Before running, preview impacted resources:

aws fis get-targets-preview \
    --experiment-template-id <your-template-id> \
    --region us-east-1


🧭 This shows which EC2, RDS, and ECS/EKS nodes in us-east-1b will be impaired.