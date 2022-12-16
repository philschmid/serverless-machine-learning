import os
from pathlib import Path
from constructs import Construct
from aws_cdk import App, Stack, Environment, Duration, CfnOutput
from aws_cdk import (
    Environment,
    Stack,
)
import aws_cdk.aws_ssm as ssm
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode, Architecture

# Environment
# CDK_DEFAULT_ACCOUNT and CDK_DEFAULT_REGION are set based on the
# AWS profile specified using the --profile option.
my_environment = Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"])


class BenchmarkLambda(Stack):
    def __init__(self, scope: Construct, construct_id: str, target_architecture="x86", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##############################
        #       Lambda Function      #
        ##############################

        # read architecture and memory size from os.environ
        architecture = os.environ.get("ARCHITECTURE", "x86_64")
        architecture = Architecture.X86_64 if architecture == "x86_64" else Architecture.ARM_64

        memory_size = int(os.environ.get("MEMORY_SIZE", 512))
        print(f"Architecture: {architecture}")
        print(f"Memory Size: {memory_size}")

        # create function
        lambda_fn = DockerImageFunction(
            self,
            "AssetFunction",
            code=DockerImageCode.from_image_asset(str(Path.cwd()), file="Dockerfile.lambda"),
            architecture=architecture,
            memory_size=memory_size,
            timeout=Duration.minutes(3),
        )
        ssm.StringParameter(
            self,
            "Parameter",
            parameter_name="/benchmark/lambda/name",
            string_value=lambda_fn.function_name,
            tier=ssm.ParameterTier.STANDARD,
        )


app = App()
rust_lambda = BenchmarkLambda(app, "BenchmarkLambda", env=my_environment)

app.synth()
