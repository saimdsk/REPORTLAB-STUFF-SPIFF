import json
from SpiffWorkflow import Workflow
from SpiffWorkflow.specs import WorkflowSpec
from serializer import NuclearSerializer


# Load from JSON
with open('nuclear') as fp:
    workflow_json = fp.read()
    serializer = NuclearSerializer()
    spec = WorkflowSpec.deserialize(serializer, workflow_json)


# Create the workflow.
workflow = Workflow(spec)
workflow.complete_all()
