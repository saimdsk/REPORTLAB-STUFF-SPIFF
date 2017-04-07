from SpiffWorkflow.specs import WorkflowSpec
from SpiffWorkflow.serializer.json import JSONSerializer

serializer = JSONSerializer()
with open('nuclear') as fp:
    workflow_json = fp.read()
spec = WorkflowSpec.deserialize(serializer, workflow_json)
