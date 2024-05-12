from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_apigatewayv2 as apigw,
    CfnOutput,
)
from aws_cdk.aws_apigatewayv2_integrations import HttpUrlIntegration, HttpLambdaIntegration
from aws_cdk.aws_iam import PolicyStatement
from constructs import Construct

class Html2ImageWithGenaiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        stage_name="demo"
        route_path="/GenAIHtmlToImage"

        lambdaRole = iam.Role(self, "Html2Image",
                              assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        lambdaRole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        
        policyBedrock = iam.Policy(self, "BedrockPolicy")  
        policyBedrock.add_statements(PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["bedrock:InvokeModel"],
            resources=["*"]
        )) 
        lambdaRole.attach_inline_policy(policyBedrock)

        # Define Lambda function
        lambda_function = _lambda.Function(
            self, "html2image-with-genai-lambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("./lambda"),
            handler="html2image.lambda_handler",
            timeout=Duration.seconds(59),
            memory_size=256,
            environment={ 
                           "MODEL_ID": "anthropic.claude-3-sonnet-20240229-v1:0"
                        },
            role = lambdaRole,

        )
        payload_format_version = apigw.PayloadFormatVersion.VERSION_1_0
        
        # Define HTTP API Gateway
        api = apigw.HttpApi(
            self, "html2image-with-genai-api",
            cors_preflight = apigw.CorsPreflightOptions(
                allow_origins=['*'],
                allow_methods=[apigw.CorsHttpMethod.GET,apigw.CorsHttpMethod.POST,apigw.CorsHttpMethod.OPTIONS],
                allow_headers=['*'],
                max_age=Duration.days(1)
            )
        )
        
        # Define HTTP API Gateway integration with Lambda
        integration = HttpLambdaIntegration(
            "html2image-with-genai-integration",
            handler=lambda_function,
            payload_format_version=payload_format_version
        )
        # Add routes to HTTP API Gateway
        api.add_routes(
            path=route_path,
            methods=[apigw.HttpMethod.ANY],
            integration=integration,
        )


        apigw.HttpStage(self, "Stage",
            http_api=api,
            stage_name=stage_name,
            auto_deploy=True
        )

        # Output the API Gateway URL
        CfnOutput(
            self, "HttpApiUrl",
            value=api.url+stage_name+route_path,
            description="HTTP API URL",
        )

