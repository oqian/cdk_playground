from aws_cdk import (
    # Duration,
    aws_lambda as _lambda,
    Stack,
    RemovalPolicy
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkPlaygroundStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_function = _lambda.Function(
            self, "HelloHandler",
            runtime=_lambda.Runtime.NODEJS_18_X,
            code=_lambda.Code.from_inline('exports.handler = async (event) => { console.log(event); return { body: "Hello World" }; };'),
            handler="index.handler",
        )

        self.lambda_function.apply_removal_policy(policy=RemovalPolicy.DESTROY)
        