🧩 Module 4 — Fargate Task CPU Stress
🎯 Purpose

This module validates the resilience of containerized workloads running on AWS Fargate under CPU pressure.
By stressing ECS Fargate tasks, we test if the PayForAdoption microservice (part of the PetSite application) remains stable and responsive even when CPU utilization spikes.

💡 Experiment Idea

Given:
The PayForAdoption microservice (within PetSite) is deployed as two ECS tasks running with the Fargate launch type.

Hypothesis:
Sustained high CPU load on one or more Fargate tasks should not cause downtime for the PetSite application.
The Pet Adoptions website should remain available, possibly with slightly higher latency.

🧱 Architecture Overview
Layer	Component	Description
Frontend	PetSite Web App	User interface for browsing and adopting pets
Microservice	PayForAdoption	Handles adoption and payment logic; deployed as ECS Fargate tasks
Cluster	ECS Cluster	Orchestrates PayForAdoption service tasks
Observability	CloudWatch + X-Ray + RUM	Tracks performance, latency, user sessions
Automation	AWS FIS	Simulates high CPU load on ECS Fargate tasks
🧩 Why PayForAdoption Matters

In the PetSite architecture, PayForAdoption is the payment microservice that ensures every adoption is recorded, billed, and confirmed.
If this service becomes slow or unresponsive, it directly impacts customer experience and business continuity.

Chaos-testing CPU load here helps ensure:

User payments aren’t blocked under stress.

Auto scaling policies are tuned correctly.

Observability tools detect and localize high-CPU anomalies quickly.