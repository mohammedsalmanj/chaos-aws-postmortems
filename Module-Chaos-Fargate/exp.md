⚙️ Experiment Setup
Step 1 — Gather ECS Cluster & Task Info

Go to ECS Console → Clusters

Locate your PayForAdoption ECS Service and note:

Cluster name (e.g., Services-PayForAdoptionCluster)

Task ARNs (2 running tasks)

These will be your FIS targets.

Step 2 — Create FIS Template

In AWS Console → Fault Injection Simulator:

Click Create experiment template

Description: ECS-FARGATE-CPU Stress Test

Name: FIS-Workshop-ECS-FARGATE-CPU-StressTest

Add Action:

Name: ECS-FARGATE-CPU-StressTest

Action type: aws:ecs:task-cpu-stress

Target: Tasks-Target-1

Action parameters:

Duration: 10 minutes

Click Save

Add Target:

Edit Tasks-Target-1

Resource type: aws:ecs:task

Target method: Resource IDs

Select the two PayForAdoption tasks

Selection scope: All

Service Access: ecs-fargate-fis-role

Stop conditions: Leave blank

Logs: Leave blank (optional)

Click Create experiment template and confirm.