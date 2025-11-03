💽 EC2 Disk Fill — Chaos Experiment Summary

In distributed systems, even simple infrastructure failures — like a disk filling up on one EC2 instance — can impact application availability.
This exercise simulates that exact condition using AWS Fault Injection Simulator (FIS) to verify application resilience under disk pressure.

🎯 Experiment Objective

Scenario: Simulate a disk fill event on one EC2 instance in a multi-AZ deployment.

Hypothesis: Disk saturation on one instance should not affect the overall application.
Traffic should reroute to healthy instances in other AZs, and the app (e.g., PetSite) should remain available.

🧩 Pre-Requisites

A running application (e.g., PetSite) deployed across multiple Availability Zones (AZs).

EC2 instance IDs of target instances (can be found in EC2 Console → Instances → Petsite).

An IAM role with FIS and SSM permissions (e.g., ec2-fis-role).

CloudWatch log group for experiment logs (e.g., /aws/fis/FisExperiments).

⚙️ AWS FIS Template Setup

In the AWS Management Console:

Go to AWS Fault Injection Simulator → Create Experiment Template

Description: EC2 Disk Fill Test

Name: FIS-Workshop-EC2-DiskFill-Test

Actions:

Click Add Action

Name: EC2-DiskFill-Test

Action Type: aws:ssm:send-command/AWSFIS-Run-Disk-Fill

Action Parameters (Document Parameters):

{"DurationSeconds":"120","Percent":"95","InstallDependencies":"True"}


Duration: 10 minutes

Targets:

Click Edit next to Instances-Target-1

Resource Type: aws:ec2:instance

Target Method: Resource IDs

Resource IDs: (enter your PetSite EC2 instance ID)

Selection Mode: All

Save Target

Service Access:

Choose an existing IAM role → ec2-fis-role

Stop Conditions: Leave blank

Logs: Send to CloudWatch Logs → select your FisExperiments log group

Create Template → Confirm creation without stop condition

🧠 Before Running the Experiment

Open AWS X-Ray → Service Map for your PetSite app

Verify normal latency (no 5xx errors)

Observe baseline request and fault rates

Check EC2 Metrics for target instances

CPU, Disk I/O, and Network are at expected healthy levels