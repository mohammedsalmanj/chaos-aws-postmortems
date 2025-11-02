# chaosawspostmortems
Documenting learning, insights, and case studies in Chaos Engineering, focusing on AWS outages and postmortem analyses. Includes practical notes, incident reviews, and best practices to improve cloud resilience and site reliability.


# AWS DNS Outage + Chaos Case Study & GameDay

This repo contains a case study of the AWS Oct2025 DNS outage and a set of GameDay / Chaos Engineering labs to practice detecting, mitigating, and recovering similar cascading failures in AWS.

Goals:
 Understand Planner/Enactor → Route53 → DynamoDB failure cascade
 Practice diagnosing DNS & controlplane outages
 Exercise common chaos scenarios: EC2 disk fill, Aurora reboot, task I/O & memory stress, EKS pod delete, AZ outage simulation
 Improve detection (CloudWatch / New Relic), runbooks, and team coordination

 # Case Study: AWS USEast DNS Outage (Oct 2025) — Executive Overview

Summary:
 Root cause: race condition between internal "Planner" and "Enactor" components that manage DNS entries (Route 53) for DynamoDB.
 Effect: empty/missing DNS records for critical controlplane endpoints → services couldn't resolve DynamoDB → EC2/autoscaling/health checks failed → large cascading outage.
 Recovery: engineers disabled aggressive automation (health checks), throttled actions, restored DNS entries, and stabilized traffic over ~15 hours.

Why this matters:
 DNS is a controlplane dependency; if it breaks, systems that are healthy appear unreachable.
