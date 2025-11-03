Chaos Experiments by Category
🧩 Compute Experiments
Module	Description	Analogy
EC2	Stop, reboot, or terminate EC2 instances	“Like turning off one worker to test if others cover.”
EC2 Disk Fill	Simulate storage exhaustion	“Phone storage full, apps start crashing.”
EC2 Latency Injection	Introduce network delay	“Like hearing your coworker respond in slow motion.”
EBS I/O Degradation	Slow disk access performance	“Like a hard drive going sluggish — takes longer to read data.”
EC2 Spot Interruptions	Simulate instance reclaim	“AWS suddenly reclaims your rented desk — how fast can you move?”
🧩 Serverless Experiments
Module	Description	Analogy
AWS Lambda Chaos	Force function timeout, error, or latency	“Like a chef who sometimes forgets an ingredient — can the kitchen recover?”
Lambda ChaosNodeLayer	Inject CPU or memory stress directly in function runtime	“Like making a chef multitask too much at once.”
🧩 Container Experiments
Module	Description	Analogy
EKS	Kill pods, simulate DNS delay, or node drain	“Cashier leaves mid-shift, but another takes over automatically.”
ECS on EC2	Kill running tasks	“Closing one kitchen station; others must pick up the orders.”
ECS Fargate	Simulate throttling or container restarts	“Overworked chef slows down but recovers soon.”
🧩 Data Experiments
Module	Description	Analogy
Aurora Instance Reboot	Simulate DB crash	“Bank’s main server rebooting during business hours.”
Aurora Cluster Failover	Promote replica to primary	“Backup branch manager takes charge instantly.”
S3 AZ1 Impairment	Isolate bucket in one AZ	“Warehouse door locked in one city, but others stay open.”
S3 AZ2 Impairment	Multi-AZ resilience test	“One warehouse offline, logistics reroute automatically.”
🧩 Network Experiments
Module	Description	Analogy
AZ Disruption	Simulate entire zone failure	“A whole city loses power; others pick up the load.”
Network Latency	Introduce packet delay or drops	“Conversations over a laggy phone line.”
DynamoDB Network Disruption	Block DynamoDB calls	“You can’t reach your main storage clerk — queues start building up.”
🧩 API Experiments
Module	Description	Analogy
API Latency/Throttling	Simulate rate limits	“Like a call center putting you on hold when it’s too busy.”
API Timeout	Drop external dependencies	“Waiting forever for someone who never replies.”