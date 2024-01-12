import os
import json
import aws_cdk as cdk
from aws_cdk import Duration
from aws_cdk.integ_tests_alpha import IntegTest, InvocationType, ExpectedResult, Match, ActualResult
import sys
import os


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
sys.path.append(SCRIPT_DIR)


from cdk_playground.cdk_playground_stack import CdkPlaygroundStack

test_app = cdk.App()

test_stack = CdkPlaygroundStack(test_app, "cdk-playground-lambda")

integ_test = IntegTest(
    test_app,
    "integ-test",
    test_cases = [test_stack]
)

integ_test.assertions.invoke_function(
    function_name = test_stack.lambda_function.function_name,
    invocation_type=InvocationType.EVENT,
    payload=json.dumps({
        "days":1
    })
).expect(
    ExpectedResult.object_like(
        {
            "execution_arn": Match.string_like_regexp("arn:aws:states:us-.*")
        }
    )
).wait_for_assertions(
    interval=Duration.seconds(10),
    total_timeout=Duration.minutes(10)
)

test_app.synth()