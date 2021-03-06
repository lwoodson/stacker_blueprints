import unittest
from stacker.context import Context
from stacker.variables import Variable
from stacker.blueprints.testutil import BlueprintTestCase

import stacker_blueprints.dynamodb

class TestDynamoDB(BlueprintTestCase):
    def setUp(self):
        self.dynamodb_variables = [
            Variable(
              'Tables',
              {
                "UserTable": {
                  "TableName": "test-user-table",
                  "KeySchema": [
                    {
                      "AttributeName": "id",
                      "KeyType": "HASH",
                    },
                    {
                      "AttributeName": "name",
                      "KeyType": "RANGE",
                    },
                  ],
                  "AttributeDefinitions": [
                    {
                      "AttributeName": "id",
                      "AttributeType": "S",
                    },
                    {
                      "AttributeName": "name",
                      "AttributeType": "S",
                    },
                  ],
                  "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                  },
                  "StreamSpecification": {
                    "StreamViewType": "ALL",
                  }
                }
              }
            )
        ]
        self.dynamodb_autoscaling_variables = [
            Variable(
              "AutoScalingConfigs",
              [
                  {
                      "table": "test-user-table",
                      "read": {"min": 5, "max": 100, "target": 75.0},
                      "write": {"min": 5, "max": 50, "target": 80.0},
                  },
                  {
                      "table": "test-group-table",
                      "read": {"min": 10, "max": 50, "scale-in-cooldown": 180, "scale-out-cooldown": 180},
                      "write": {"max": 25},
                  },
              ]
            )
        ]

    def test_dynamodb_table(self):
        ctx = Context({'namespace': 'test', 'environment': 'test'})
        blueprint = stacker_blueprints.dynamodb.DynamoDB('dynamodb_table', ctx)
        blueprint.resolve_variables(self.dynamodb_variables)
        blueprint.create_template()
        self.assertRenderedBlueprint(blueprint)

    def test_dynamodb_autoscaling(self):
        ctx = Context({'namespace': 'test', 'environment': 'test'})
        blueprint = stacker_blueprints.dynamodb.AutoScaling('dynamodb_autoscaling', ctx)
        blueprint.resolve_variables(self.dynamodb_autoscaling_variables)
        blueprint.create_template()
        self.assertRenderedBlueprint(blueprint)
