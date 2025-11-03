

🌀 chaos-aws-postmortems

Documenting real-world outages, resilience failures, and recovery patterns — with a focus on AWS control planes, chaos engineering, and observability.

This repository transforms real AWS incidents into hands-on chaos labs, helping teams strengthen reliability through:

GameDays 🕹️

Observability exercises 🔬

Fault injection experiments ⚙️

🎯 The goal isn’t to break things for fun — it’s to understand how things break,
so we can make them unbreakable.

📘 Purpose

Cloud reliability doesn’t come from tools — it comes from practice.
This repo acts as a training ground for SRE, DevOps, and AIOps engineers to:

✅ Study how AWS outages actually unfold
✅ Simulate them safely in local or AWS environments
✅ Practice diagnosis, communication, and recovery
✅ Improve monitoring, automation, and runbooks

Each case study links together:

A real-world AWS outage

A relatable analogy 💡

A reproducible chaos experiment 💥

🧩 Repository Structure
Section	Description
Case Studies	Real AWS incident postmortems (DNS, EC2, Aurora, EKS, S3, etc.)
Chaos Experiments	Fault injection using AWS FIS or local simulators
Resilience Practices	Runbooks, recovery drills, and alerting patterns
Observability Layers	Using CloudWatch, X-Ray, and New Relic for MELT data (Metrics, Events, Logs, Traces)
GameDays	Controlled drills simulating AWS control plane failures

Each module helps answer:

🔍 What failed?
💥 Why did it spread?
🧠 What would we do differently next time?

🧩 Case Study: AWS US-East DNS Outage (October 2025)
🧠 1. Why DNS Is So Critical

Every AWS service relies on DNS to translate names like:

dynamodb.us-east-1.amazonaws.com → 10.23.40.18


If DNS fails, apps lose their ability to communicate — even if the backend is healthy.

💡 Analogy:
DNS is like the phonebook of AWS.
When the phonebook goes blank, everyone still exists — but no one can call each other.
Services start retrying, crashing, or looping endlessly.

⚙️ 2. The Hidden Mechanism — Planner and Enactor
Component	Role	Analogy
Planner	Decides which DNS records to change	🧠 The manager writing tasks on a whiteboard
Enactor	Executes and validates the DNS updates	🧰 The technician performing the work

When both stay in sync, AWS’s DNS is accurate.
If they drift apart — chaos begins.

💥 3. What Went Wrong — The Race Condition

During a DNS sync update in October 2025:

The Planner generated DNS updates rapidly (due to DynamoDB scaling).

The Enactor lagged behind.

The Planner thought updates were complete and sent blank records.

Route 53 applied those blanks — deleting valid DNS entries.

💡 Analogy:
The manager erased the whiteboard too soon — the technician hadn’t copied the info yet.
Result: half the names vanished.

🌊 4. The Domino Effect — How One Bug Cascaded Across AWS

Step 1: DynamoDB “disappeared.”
→ EC2, Lambda, and internal tools couldn’t resolve DynamoDB endpoints.

Step 2: Auto Scaling panicked.
→ Health checks failed → instances terminated → endless loop of broken replacements.

Step 3: Control plane overloaded.
→ Retry storms flooded IAM, S3, CloudFormation, CloudWatch, and even AWS’s status page.

💡 Analogy:
The phonebook vanished — people started driving to each other’s offices to talk,
causing a traffic jam of retries.

📉 5. Impact Summary
Category	Details
Region	us-east-1 (ripple effects globally)
Duration	~15 hours
Affected Services	Route 53, DynamoDB, EC2, Auto Scaling, IAM, S3
Customer Symptoms	503 errors, failed scaling, stuck CloudFormation, login failures
Root Cause	Race condition between Planner & Enactor deleting internal Route 53 records

💡 Analogy: Healthy systems looked sick — like patients misdiagnosed because the hospital lost their records.

🧰 6. AWS’s Recovery Process

🛑 Stopped the Planner automation

🔁 Restored missing DNS records manually

🧩 Throttled auto-scaling to stop instance churn

🔍 Validated DNS zones for consistency

🧱 Deployed handshake validation to prevent overwrite mismatches

⏳ Recovery took hours — not from fixing the bug, but due to DNS cache propagation delays.

🔍 7. Observability & Detection
Tool	What It Showed
CloudWatch	Spikes in Route 53 errors & EC2 health check failures
New Relic	Dependency maps showing DynamoDB/Route 53 red (unreachable)
X-Ray	Traces failed during DNS resolution
CloudTrail	Surge in termination and retry events
RUM	Increased latency and user 503s

Observation: DNS outages look like app failures until traced upstream.

🧠 8. Lessons Learned
Area	Lesson	Action
Control Plane Awareness	DNS is not background plumbing.	Include DNS mapping in design reviews.
Automation Safety	Overactive automation amplifies failure.	Add pause and backoff logic.
Observability	Metrics alone can mislead during cascading failures.	Correlate logs, traces, and MELT.
Preparedness	Teams must drill DNS outages.	Run quarterly GameDays.
💬 9. Simplified Analogy — “The City Lost Its Phonebook”

Imagine AWS as a city:

Buildings = Services (Police HQ, Hospital, Power Station)

Phonebook = Route 53

During maintenance, the phonebook team erases half the entries.
Now no one can call anyone.
People rush around trying to connect manually — chaos everywhere.

Once the phonebook is rebuilt, the city starts functioning again.
It wasn’t a power failure — it was a communication breakdown.

🔄 10. Why This Case Matters

This outage proved that:

🧩 “Healthy but unreachable” is a real failure mode.

Systems don’t need to crash — they just need to stop talking.

Resilience isn’t about zero downtime —
It’s about failing safely, detecting quickly, and recovering gracefully.

Future designs must:

Cache DNS responses safely

Use secondary resolvers

Detect dependency failures early

Prevent automation from compounding chaos

🧠 In Short

“We don’t just document AWS outages — we relive them safely.”
Each failure is a chance to learn how complex systems behave under stress.

This repo module and related experiments were inspired by the
AWS Resilience Workshop - https://catalog.us-east-1.prod.workshops.aws/workshops/eb89c4d5-7c9a-40e0-b0bc-1cde2df1cb97/en-US/environment/bring-your-own

