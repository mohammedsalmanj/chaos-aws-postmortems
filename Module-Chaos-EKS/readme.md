Module: EKS Pod Delete (via AWS FIS Scenario)
🎯 Objective

Simulate the accidental termination (delete) of application pods in an Amazon EKS cluster and measure how your system responds — focusing on recovery time, session continuity, and user impact.

🧠 Experiment Idea

Kubernetes pods can be terminated or evicted for various reasons — node maintenance, spot interruption, resource pressure, or rolling updates.

In this chaos test, we’ll intentionally delete pods using the new AWS Fault Injection Service (FIS) Scenarios feature, announced Nov 7, 2024, to observe how resilient our app is to pod-level restarts.

Hypothesis:
Restarting the pods should have no customer impact, since the cold boot time is only ~5 seconds, and traffic should shift seamlessly to healthy pods.

🧩 Environment Setup
Component	Description
EKS Cluster	PetSite (2 running pods for frontend website)
Namespace	default
App Selector Label	app=petsite
Service Account	eks-fis-role
Observability	CloudWatch, X-Ray, CloudWatch RUM
FIS Scenario	EKS Pod Delete (GA released scenario)
⚙️ Step 1: Collect EKS Info

Open EKS Console → Clusters → PetSite

Go to Resources → Workloads → Pods

Identify:

Namespace → default

Label → app=petsite

Cluster ARN

Confirm 2 pods are active and healthy.

⚙️ Step 2: Create FIS Experiment Template Using Scenario

Go to AWS FIS Console → Scenario Library

Search for “EKS Pod Delete”

Click Create template with scenario

You’ll see a pre-filled template that defines:

Action: Delete Kubernetes Pods

Target: Based on namespace + label selector

⚙️ Step 3: Configure Parameters

Click Shared Parameters and add the following:

Parameter	Value
appSelector	app=petsite
clusterArn	<Your PetSite Cluster ARN>
kubernetesServiceAccount	eks-fis-role
targetNamespace	default

Then click Save Shared Parameter.

⚙️ Step 4: Service Access and Logging

Under Service Access, choose:

✅ Use existing IAM Role → eks-fis-role

Enable CloudWatch Logs

Log group: FISExperiments

Click Create Experiment Template

Confirm creation without stop conditions

🧪 Validation Procedure
🧾 Define Steady State

Before running the experiment:

Open CloudWatch → X-Ray → Trace Map

Record:

Average Latency

Request rate

Fault count (should be 0)

This defines your steady-state baseline — normal system behavior before injecting chaos.