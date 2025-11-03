🧠 Experiment Execution
Step 1 — Start the Workflow
STATE_MACHINE_ARN=$(aws stepfunctions list-state-machines \
  --query "stateMachines[?contains(name,'SpotChaosStateMachine')].stateMachineArn" \
  --output text)

aws stepfunctions start-execution \
  --state-machine-arn ${STATE_MACHINE_ARN} \
  --input '{ "JobDuration": "6", "CheckpointDuration": "2" }'

Step 2 — Start the FIS Experiment
SPOT_EXPERIMENT_TEMPLATE_ID=$(aws fis list-experiment-templates \
  --query "experimentTemplates[?tags.Name=='FisWorkshopSpotTerminate'].id" \
  --output text)

aws fis start-experiment \
  --experiment-template-id $SPOT_EXPERIMENT_TEMPLATE_ID \
  --tags Name=FisWorkshopSpotTerminateTest


📊 Validation Procedure

Open CloudWatch → Dashboard named FisSpot-<region>

Set duration to 15 minutes

Observe:

CPU/network drop on terminated instance

New instance launch (Spot replacement)

Step Functions job resumes from last checkpoint