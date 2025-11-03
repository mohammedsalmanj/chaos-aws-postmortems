🧩 How to Use
Option 1 — AWS CLI

Save this file as az-power-interruption.json, then run:

aws fis create-experiment-template \
  --cli-input-json file://az-power-interruption.json \
  --region us-east-1


You’ll get a response like:

{
  "experimentTemplate": {
    "id": "fis-0abcd1234ef567890",
    "state": "active"
  }
}

Option 2 — Run Target Preview

Before executing, verify which resources are targeted:

aws fis get-targets-preview \
  --experiment-template-id fis-0abcd1234ef567890 \
  --region us-east-1


✅ This shows which EC2, RDS, ECS, or EKS resources in us-east-1b will be impacted.

Option 3 — Start the Experiment
aws fis start-experiment \
  --experiment-template-id fis-0abcd1234ef567890 \
  --tags Name="us-east-1b AZ Execution 1"


Confirm with:

aws fis list-experiments --region us-east-1

⚙️ Parameters Explained
Parameter	Description
affectedAz	The Availability Zone to impair (us-east-1b)
affectedRolesForInsufficientCapacityException	Dummy IAM role placeholder (required by scenario)
targetingTags	Resources with AzImpairmentPower=Ready will be targeted
dnsImpactDuration	How long DNS impact lasts (2 min)
outageDuration	Simulated outage duration (10 min)
recoveryDuration	Time for recovery simulation (5 min)
reportConfiguration	Exports PDF report to S3 and includes CloudWatch Dashboard metrics
roleArn	IAM execution role for FIS
logConfiguration	Sends logs to CloudWatch log group
🧠 Key Notes

All PetSite resources (ECS, RDS, EKS, EC2) should be tagged with:

Key = AzImpairmentPower
Value = Ready


The dummy role (FisServerless-FISDummyRoleForASG...) is only for scenario completeness; it isn’t used directly.

The AvailabilityZonePowerImpairment CloudWatch Dashboard tracks latency, errors, and request flow during the event.

The experiment lasts roughly 15–20 minutes including recovery and post-experiment metrics.

🧩 Expected Behavior

✅ EC2 / EKS / ECS capacity in us-east-1b temporarily lost
✅ Auto Scaling replaces instances in other AZs
✅ RDS fails over to healthy AZ
✅ Application traffic reroutes automatically via ALB
⚠️ Minor latency spike + few transient 5xx errors