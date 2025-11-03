Technical Overview

Objective:
Simulate EC2 instance failures such as disk saturation, CPU exhaustion, or network loss to evaluate autoscaling, alerting, and service continuity.

🧩 Why This Matters

In cloud environments, EC2 instances are your foundational compute layer.
Even though AWS manages the infrastructure, issues like:

Disk filling up due to logs,

High CPU due to rogue processes,

Stuck network packets due to app misconfigurations,
can still cripple your application.

Chaos Engineering helps you ensure that one broken EC2 doesn’t become a customer outage.