Module: Aurora Instance Reboot
🎯 Objective

Understand the impact of rebooting an Amazon Aurora instance within a Multi-AZ cluster and verify that the application continues operating without disruption.

🧠 Experiment Idea

During regular operations, you might need to reboot one or more Aurora DB instances — for example:

When modifying or applying a new parameter group.

When performing maintenance or patch updates.

In this chaos experiment, we’ll simulate such a reboot using AWS Fault Injection Service (FIS) to validate:

How Aurora handles temporary unavailability of a reader instance.

Whether the application continues serving traffic using the writer instance.

How quickly the reader instance recovers and rejoins the cluster.

🧩 Hypothesis

Rebooting the reader instance will make it temporarily unavailable,
but traffic should failover to the writer instance,
and the application should not experience errors or downtime.
The reader instance should automatically recover after reboot.

🧱 Setup Overview

Given:

A Multi-AZ Aurora Cluster (PostgreSQL/MySQL) with:

1 Writer instance

1 Reader instance

An ECS service running a load generator simulating application traffic

AWS X-Ray and CloudWatch monitoring in place for tracing

Tool: AWS Fault Injection Service (FIS)

⚙️ Experiment Setup
1. Create Experiment Template

Open the AWS FIS Console → Create Experiment Template

Fill in:

Description: RebootRDSAurora

Name Tag: FisWorkshopRds

2. Define Action

Click Add Action

Name: RebootRDSAurora

Action Type: aws:rds:reboot-db-instances

Target: Default (DBInstances-Target-1)

Click Save

🧠 Note:
We are using a Multi-AZ Aurora cluster but we don’t want to trigger a failover —
the goal is to observe reader reboot behavior only.

3. Select Target

Go to RDS Console → find your cluster → identify the Reader instance (Role = Reader).

Back in FIS, under Targets, edit DBInstances-Target-1.

Set:

Resource type: aws:rds:db

Target method: Resource IDs

Select your Reader DB Instance ID

Selection mode: All

Click Save

4. Configure Service Access

In Service Access, choose:

Use existing IAM role

Select your previously created rds-fis-role

In Logs, enable:

✅ “Send to CloudWatch Logs”

Choose log group: FISExperiments

Finally, click Create Experiment Template.
When prompted, confirm creation without stop conditions.

🧪 Validation Procedure
1. Define Success Criteria

The experiment is successful if:

The application continues serving traffic normally.

X-Ray shows no spike in Faults during the reader reboot.

The reader instance recovers automatically and rejoins the cluster.

2. Pre-Check Application

Confirm the ECS load generation service is running correctly.

In AWS X-Ray, open the Trace Map for your app → observe normal operation.
You’ll use this later to check if any faults appear during the reboot.