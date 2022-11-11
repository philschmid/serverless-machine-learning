import os
from pathlib import Path
from constructs import Construct
from aws_cdk import App, Stack, Environment, Duration, CfnOutput
from aws_cdk import (
    Environment,
    Stack,
    aws_iam as iam,
    aws_apigateway as _apigw,
)
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode, Architecture, FunctionUrlAuthType
from aws_cdk.aws_logs import RetentionDays

# Environment
# CDK_DEFAULT_ACCOUNT and CDK_DEFAULT_REGION are set based on the
# AWS profile specified using the --profile option.
my_environment = Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"])


class GradioLambda(Stack):
    def __init__(self, scope: Construct, construct_id: str, target_architecture="x86", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##############################
        #       Lambda Function      #
        ##############################

        architecture = Architecture.ARM_64 if target_architecture == "arm" else Architecture.X86_64
        # create function
        lambda_fn = DockerImageFunction(
            self,
            "AssetFunction",
            code=DockerImageCode.from_image_asset(str(Path.cwd().joinpath("containers")), file="Dockerfile.lambda"),
            architecture=architecture,
            memory_size=8192,
            timeout=Duration.minutes(1),
        )
        # add HTTPS url
        fn_url = lambda_fn.add_function_url(auth_type=FunctionUrlAuthType.NONE)
        CfnOutput(self, "functionUrl", value=fn_url.url)

        ##############################
        #         API Gateway        #
        ##############################

        # api = _apigw.LambdaRestApi(
        #     self,
        #     "hf_api_gw",
        #     proxy=True,
        #     handler=lambda_fn,
        #     default_cors_preflight_options=_apigw.CorsOptions(
        #         allow_origins=_apigw.Cors.ALL_ORIGINS, allow_methods=_apigw.Cors.ALL_METHODS
        #     ),
        # )
        # route = api.root.add_resource("signup")
        # route.add_method("POST")  # POST /signup


app = App()
rust_lambda = GradioLambda(app, "GradioLambda", env=my_environment)

app.synth()
