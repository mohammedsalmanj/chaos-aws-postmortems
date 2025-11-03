🚀 Run the Experiment

In AWS FIS → Experiment Templates, select your template.

Add a tag:

Name: EKS_POD_DELETE_11072025-x

Click Start Experiment

Confirm “State” changes to Running

📡 Observe During Experiment

While the experiment runs:

Open CloudWatch Container Insights → EKS → Nodes/Pods

Observe:

Pods being terminated

New pods being created by the Deployment controller

You’ll see your PetSite pods momentarily disappear, then respawn.

🔍 Analyze Results

Check the following dashboards:

Tool	What to Observe
CloudWatch X-Ray	Trace Map for spikes in Faults or latency
CloudWatch RUM	Frontend user session errors or reconnect events
ECS / EKS Console	Pod deletion + recreation events
Logs	Pod restarts visible in application or container logs
💡 Outcome

Our hypothesis turned out wrong 😅

While Kubernetes successfully restarted the pods,
our frontend sessions were interrupted — users had to reconnect.

This confirms that:

The backend recovered automatically ✅

But client experience suffered due to session loss ❌

📈 Findings Summary
Metric	Observation	Impact
Pod Restart Time	~5 seconds	Minimal
App Recovery	Automatic	✅
User Session	Interrupted	❌
Faults (5xx)	Temporary spike	⚠️ Minor
Hypothesis Result	Partial failure	Needs session resilience fix
💬 Analogy

Think of your EKS pods like restaurant waiters 🍽️
You fire one to test if the team can still serve customers.

Another waiter quickly joins (new pod),
but some customers lose their tab (session).
The restaurant (cluster) stays open,
but service continuity suffers until reconnection.

🧠 Lessons Learned
Area	Lesson	Action
Resilience	Kubernetes handled pod termination gracefully	✅ Validate HPA scaling for more robustness
User Experience	Clients lost session state during restart	🔄 Implement session persistence (Redis/ElastiCache)
Observability	FIS + X-Ray helped isolate frontend vs backend impact	📊 Integrate RUM & X-Ray dashboards
Chaos Practice	Scenario-based chaos makes EKS validation simpler	⚙️ Add to regular GameDay cycles
🧰 Tools Used
Category	Tool
Chaos Simulation	AWS FIS Scenario — EKS Pod Delete
Kubernetes Cluster	Amazon EKS (PetSite app)
Observability	CloudWatch, X-Ray, CloudWatch RUM
Service Account	eks-fis-role
Logs	FISExperiments log group
🧩 Outcome Summary

✅ FIS successfully deleted pods
✅ Kubernetes automatically recreated them
⚠️ Minor service interruption observed
💡 Next improvement — session persistence + graceful reconnect