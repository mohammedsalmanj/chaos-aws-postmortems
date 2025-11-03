🧩 Module 3 — Baselining: EC2 Spot Instance Termination
🎯 Purpose

This module establishes a baseline for how a distributed workload behaves when a Spot Instance is suddenly terminated.
You’ll test how well your workflow can recover from interruptions when checkpoints are enabled, validating the self-healing behavior of AWS Step Functions and EC2 Spot.

💡 Experiment Idea

Given:
An AWS Step Functions workflow orchestrates compute jobs on EC2 Spot Instances and restarts them until the job completes (100 %).

Hypothesis:
Terminating a running Spot Instance should cause extra computation time but the job will eventually reach 100 % completion without manual intervention.

🧱 Architecture Overview
Layer	Component	Description
Workflow Engine	AWS Step Functions	Orchestrates compute tasks with checkpoints
Compute Layer	EC2 Spot Instances	Performs processing; target for termination
Storage / Checkpointing	Amazon S3 / DynamoDB	Stores intermediate job state
Observability	CloudWatch + FIS Logs	Track job duration, restarts, and termination impact
Automation	AWS Fault Injection Simulator (FIS)	Triggers controlled instance termination
⚙️ FIS Template Setup
Step	Setting	Value
Description		Use EC2 terminate instances on Spot instance
Name		FisWorkshopSpotTerminate
Role		FisWorkshopSpotRole
Log Group		/aws/fis/FisExperiments
Action 1 — AllowSomeCompletion (Wait Action)

Action Type: aws:fis:wait

Parameters: "duration": "180" # 3 minutes

Purpose: Wait for partial progress before interruption

Action 2 — Terminate Spot Instance

Action Type: aws:ec2:terminate-instances

Name: FisWorkshopSpot-TerminateInstance

Description: Terminate selected Spot instances after wait period

Start After: AllowSomeCompletion

Target

Resource Type: aws:ec2:instance

Target Method: Resource IDs

Resource IDs: (enter your Spot instance ID)

Selection Mode: All

Logging & Access

IAM Role: FisWorkshopSpotRole

CloudWatch Logs: Send to FisExperiments

Stop Conditions: None