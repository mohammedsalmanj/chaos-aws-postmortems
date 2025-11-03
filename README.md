🌀 chaos-aws-postmortems

Documenting real-world learning, insights, and case studies in Chaos Engineering — with a special focus on AWS outages, control plane failures, and resilience testing.
This repository turns real incidents into hands-on labs, helping teams build stronger systems through GameDays, observability exercises, and chaos experiments.

🎯 The goal isn’t to break things for fun — it’s to understand how things break,
so we can make them unbreakable.


📘 Purpose

Cloud reliability doesn’t come from theory or tools — it comes from practice.
This repo acts as a learning ground for SREs, DevOps, and AIOps engineers to:

Study how AWS outages actually unfold

Simulate them in a safe environment

Practice diagnosis, communication, and recovery

Improve automation, monitoring, and response playbooks

Each case study connects:

A real AWS outage or scenario

An analogy anyone can understand

A chaos experiment you can recreate



We explore AWS outages and fault domains through:

🧩 Case Studies — Postmortems of real AWS incidents (DNS, EC2, Aurora, EKS, S3, etc.)

⚙️ Chaos Experiments — Fault Injection (via AWS FIS / local tools)

🧠 Resilience Practices — Runbooks, alerting improvements, and detection patterns

🔬 Observability Layers — Using CloudWatch, X-Ray, and New Relic for MELT data (Metrics, Events, Logs, Traces)

🎮 GameDays — Repeatable, controlled drills that simulate real outage conditions

Each module is built to answer three questions:

What failed?

Why did it spread?

What would we do differently next time?


🧩 Case Study: AWS US-East DNS Outage (October 2025)

How a small synchronization fault between AWS’s internal DNS systems triggered a massive, multi-service disruption — and what we can learn from it.

🧠 1. Why DNS Is So Critical

Before diving into what broke, it’s important to understand why DNS is so central.
Every app and AWS service relies on DNS to translate a name into a reachable address.

For example:

dynamodb.us-east-1.amazonaws.com → 10.23.40.18


Your app doesn’t know where DynamoDB lives — it just knows this name.
If that translation fails, the app can’t reach its database.
Even if DynamoDB is healthy, to the app it looks dead.

💡 Analogy: DNS is like the phonebook of AWS.
When the phonebook goes blank, everyone still exists — but no one can call each other.
Services start retrying, crashing, or spinning in loops because they think the other side vanished.

This is why Route 53, AWS’s DNS service, is more than a public resolver —
it’s part of AWS’s internal control plane, powering communication between systems like EC2, DynamoDB, CloudWatch, and IAM.

⚙️ 2. The Hidden Mechanism — Planner and Enactor

Inside AWS, DNS updates happen dynamically.
As AWS scales up and deploys services, thousands of DNS records are created, updated, or deleted every minute.

This process is managed by two internal components:

Component	Role	Analogy
Planner	Decides what DNS records need to be changed. It creates a “to-do” list of updates for Route 53.	🧠 The manager who writes tasks on a whiteboard.
Enactor	Executes those updates — applying changes to Route 53 and verifying them.	🧰 The technician who actually performs the updates.

When both stay synchronized, AWS’s internal DNS stays accurate and stable.
If they drift apart — bad updates can spread quickly.

💥 3. What Went Wrong — The Race Condition

During a normal update cycle in October 2025, AWS rolled out a new DNS synchronization routine.

The Planner started generating DNS updates at high frequency to reflect scaling in DynamoDB partitions.

The Enactor fell slightly behind due to throttling in its internal queue.

The Planner assumed those old entries were processed and sent “blank” updates for them.

Route 53 applied those empty updates, effectively deleting valid DNS entries for key internal services — especially DynamoDB control plane endpoints.

💡 Analogy: Imagine the manager updates the whiteboard too fast, thinking the technician already copied it down.
The technician, confused, erases names assuming they’re done.
Suddenly, no one knows who’s assigned to what — the board is blank.

🌊 4. The Domino Effect — How One Bug Cascaded Across AWS

Once DNS records disappeared, the problem wasn’t isolated — it cascaded across many AWS systems:

Step 1: DynamoDB “disappeared”

EC2, Lambda, and internal AWS tools couldn’t resolve dynamodb.us-east-1.amazonaws.com.

These services depend on DynamoDB for configuration, state tracking, and health data.

Step 2: Auto Scaling went into a loop

Health checks couldn’t reach DynamoDB.

EC2 instances were marked as unhealthy and terminated.

New instances came up, but faced the same DNS failure — creating a loop of useless replacements.

Step 3: Control plane overload

The failed health checks triggered retries, API calls, and internal updates at scale.

These retries flooded internal networks, slowing down IAM, S3, CloudFormation, and CloudWatch APIs.

Even AWS’s status page began lagging — classic control plane congestion.

💡 Analogy: It was like a city where the phonebook vanished.
People started driving to each other’s offices to talk, creating traffic jams.
In AWS’s case — those “traffic jams” were retry storms.

📉 5. Impact
Category	Impact
Affected Region	us-east-1 (primary), ripple effects globally
Duration	~15 hours until full recovery
Services Hit	Route 53, DynamoDB, EC2, Auto Scaling, IAM, S3
Customer Symptoms	API 503s, failed EC2 scaling, stalled CloudFormation stacks, console login failures
Root Cause	Race condition between DNS Planner and Enactor, leading to deletion of internal Route 53 records

💡 Analogy: Healthy systems looked sick — like patients misdiagnosed because the hospital’s record system lost their names.

🧰 6. AWS’s Recovery Process

Stopped the Planner automation – to prevent more blank DNS updates.

Manually restored DNS records – re-created missing entries for DynamoDB and other control plane services.

Throttled auto-scaling and health checks – stopped unnecessary EC2 terminations.

Validated DNS zones – ensured consistency between Planner and Enactor records.

Deployed permanent fixes – added handshake validation so Planner and Enactor can’t overwrite valid entries again.

Recovery took time mainly due to DNS propagation — even once fixed, cached clients and instances took hours to relearn correct entries.

🔍 7. Observability and Detection
Tool	What It Showed
CloudWatch	Spikes in Route 53 resolution errors and EC2 health check failures
New Relic	Dependency maps showing DynamoDB and Route 53 red (unreachable)
X-Ray	Traces failing at DNS resolution stage
CloudTrail	Surge in Auto Scaling termination events
RUM	Increased frontend latency and user errors (503s)

Observability teams noted that DNS failures initially looked like app-level issues — a reminder to always trace issues upstream to dependencies.

🧠 8. Lessons Learned
Area	Lesson	Action
Control Plane Awareness	DNS is not background plumbing — it’s a core dependency.	Map DNS dependencies in system design reviews.
Automation Safety	Overactive automation can multiply impact.	Build safety levers (pause, backoff) into automation flows.
Observability	Pure metrics can mislead during cascading outages.	Use correlation (logs, traces, MELT).
Preparedness	Teams need DNS outage drills.	Run quarterly GameDays focused on control plane dependencies.
💬 9. Simplified Analogy — “The City Lost Its Phonebook”

Imagine AWS as a big connected city:

Every building (service) has a name: “Police HQ,” “Hospital,” “Power Station.”

The city’s phonebook (Route 53) tells everyone how to reach each other.

One night, during maintenance, the team updating the phonebook accidentally erases half the entries.
Now:

The police can’t call the hospital.

Power stations can’t signal control.

Everyone starts panicking, restarting systems, and creating more confusion.

Eventually, the city freezes — not because buildings collapsed, but because communication did.
When engineers manually rebuild the phonebook, everything starts flowing again.

🔄 10. Why This Case Matters

This outage showed that:

“Healthy but unreachable” is a real failure mode.

Systems don’t need to crash — they just need to stop talking.

Resilience isn’t about zero downtime — it’s about failing safely and recovering fast.

Understanding these dependencies helps engineers design systems that:

Cache DNS safely,

Failover to secondary resolvers,

Detect dependency issues early,

And avoid automation loops that worsen impact.

