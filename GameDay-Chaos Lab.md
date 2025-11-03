🎮 GameDay / Chaos Lab: Simulating the AWS DNS Outage
🎯 Objective

Re-create a DNS resolution failure similar to the Oct 2025 AWS US-East incident,
observe how applications behave when they can’t reach a dependency,
and practice restoring service without causing additional damage.

🧱 Lab Setup

Choose one of two environments:

Option	Environment	Tools Used
A. Local (Docker)	Simple micro-service app + internal DNS container	Docker Compose, CoreDNS, New Relic Agent
B. AWS Sandbox	EC2 + Route 53 Private Hosted Zone	AWS FIS ( Fault Injection Simulator ), CloudWatch, X-Ray, New Relic

Both options follow the same flow:
1️⃣ Run a healthy app → 2️⃣ Break DNS → 3️⃣ Observe metrics → 4️⃣ Recover → 5️⃣ Review alerts.

⚙️ Step 1 — Normal Operation (Baseline)

Application:
A tiny Python or Node.js web app calling DynamoDB (or a mock DB API).

curl http://app.local/ping-db
# → 200 OK  (DB reachable)


Verify Metrics:

CloudWatch → DNSResolutionTime ~ few ms

New Relic → Green dependency graph

X-Ray → Full trace reaching DB endpoint

💥 Step 2 — Inject DNS Failure
🔸 Local Option

Simulate broken resolver:

# Stop DNS resolver in app container
docker exec app bash -c "echo 'nameserver 127.0.0.2' > /etc/resolv.conf"
curl http://app.local/ping-db
# → Could not resolve host

🔸 AWS Option (FIS)

Create an FIS experiment that blocks outbound 53 traffic:

{
  "description": "Simulate DNS outage by blocking port 53",
  "targets": { "Instances": { "resourceType": "aws:ec2:instance",
    "resourceTags": { "ChaosTarget": "true" }, "selectionMode": "COUNT(1)" } },
  "actions": {
    "BlockDNS": {
      "actionId": "aws:ssm:send-command",
      "parameters": {
        "documentName": "AWSFIS-RunShellScript",
        "documentParameters": { "commands": ["iptables -A OUTPUT -p udp --dport 53 -j DROP"] }
      },
      "targets": { "Instances": "Instances" }
    }
  },
  "roleArn": "arn:aws:iam::<ACCOUNT_ID>:role/FISExperimentRole",
  "stopConditions": [{ "source": "none" }]
}


Run it:

aws fis start-experiment --experiment-template-id <template_id>

🔍 Step 3 — Observe Impact
Layer	Expected Signal	Analogy
App Logs	Temporary failure in name resolution	App forgot everyone’s phone number
CloudWatch	Route 53 errors ↑ , HTTP 5xx ↑	Calls failing before leaving app
New Relic APM	Red dependency line to DB	Broken link on service map
X-Ray	Trace halts at DNS segment	Conversation ends mid-sentence

🧩 Analogy: The app keeps trying to call the database, but its “contact list” vanished — it just keeps redialing the void.

🧰 Step 4 — Recover and Validate

Local Recovery

docker exec app bash -c "echo 'nameserver 8.8.8.8' > /etc/resolv.conf"


AWS Recovery

aws ssm send-command \
--targets "Key=tag:ChaosTarget,Values=true" \
--document-name "AWS-RunShellScript" \
--parameters '{"commands":["iptables -F"]}'


Validate

curl http://app.local/ping-db
# → 200 OK


Metrics should return to baseline; ALB health checks turn green.

📈 Step 5 — Review and Debrief
Question	Discussion Point
Detection Time	How quickly did alerts fire?
Alert Context	Did you know it was DNS, or just “DB unreachable”?
Automation Behavior	Did autoscaling or retries make it worse?
Recovery Speed	How long to restore connectivity?
Communication	Who got notified first — infra or app team?

Record outcomes in your postmortem notes folder:
/postmortems/dns-outage-gameday-YYYYMMDD.md

🧠 Learning Outcomes
Theme	Takeaway
Dependency Awareness	Apps fail not because of logic, but missing names.
Monitoring	Correlate DNS failures ↔ app errors.
Automation	Build “pause and inspect” into health checks.
Resilience	Use cached resolvers / fallback endpoints.

💬 Analogy:
Practicing this GameDay is like doing fire drills for your cloud —
everyone knows the exits before the smoke shows up.