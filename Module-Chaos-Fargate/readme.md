🧠 Understand Steady State

Before starting the experiment:

Open CloudWatch → Container Insights → PayForAdoption service

Observe baseline CPU utilization and task count.

Check X-Ray Trace Map for PetSite — confirm all requests succeed and latency is normal.

🚀 Run the Experiment
aws fis create-experiment-template \
  --cli-input-json file://fis-template-ecs-fargate-cpu-stress.json

aws fis start-experiment \
  --experiment-template-id <template_id> \
  --tags Name=ECS_FARGATE_Task_CPU_$(date +%Y%m%d-%H%M)


Monitor:

In FIS Console, state → Running

In CloudWatch, CPU utilization → spikes toward 90–100%

In X-Ray, latency ↑ slightly but no 5xx faults

🌐 Validate Application Availability

Get PetSite URL:

export MYSITE=$(aws ssm get-parameter --name '/petstore/petsiteurl'  | jq -r .Parameter.Value | tr '[:upper:]' '[:lower:]' | cut -f 3 -d '/')
echo "http://$MYSITE"


Open in browser → simulate normal user flow:

Browse pets

Adopt multiple pets

Pay for adoption

Then track your user sessions in CloudWatch RUM to confirm user journeys are still functional.

📊 Observation
Signal	Observation	Meaning
Container Insights	CPU ↑ to 90–100% on stressed tasks	Expected load saturation
X-Ray Latency	Slight increase	CPU throttling but service still responds
CloudWatch RUM	No user session drop	Frontend unaffected
ALB Target Health	All healthy	ECS managed load correctly
🧾 Learning & Improvements
Theme	Key Takeaway
Resilience	High CPU on one task didn’t impact user experience — tasks are well isolated.
Scaling Policy	ECS service maintained stability with two tasks; scaling out could further reduce latency.
Observability	Container Insights and X-Ray provided clear visibility into stress behavior.
Chaos Readiness	CPU pressure validated Fargate’s burst and throttling tolerance.
💬 Analogy

Think of each Fargate task as a checkout counter in a pet store.
If one counter’s staff gets overwhelmed (CPU stress), customers naturally line up at the other counter — the store (your app) keeps running.

🧹 Cleanup

If you wish to remove the experiment:

aws fis delete-experiment-template \
  --id <template_id>


✅ This module confirms your containerized microservices remain reliable under CPU saturation and that ECS + Fargate + ALB maintain graceful degradation instead of downtime.