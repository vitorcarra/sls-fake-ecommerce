from typing import Dict
from aws_cdk import (
    aws_iam,
    aws_rds as rds,
    aws_ec2 as ec2,
    core,
    aws_lambda
)
from aws_cdk.core import CustomResource
import aws_cdk.custom_resources as cr


from .postgres import PostgresRds
from utils.stack_util import add_tags_to_stack

class DataStack(core.Stack):
    vpc: ec2.IVpc

    def __init__(self, app: core.Construct, id: str, config: Dict, vpc: ec2.Vpc, rds_sg_id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)


        add_tags_to_stack(self, config)

        rds_sg = ec2.SecurityGroup.from_security_group_id(
            self,
            "PostgresSg",
            security_group_id=rds_sg_id
        )

        rds_instance = PostgresRds(self, 'PostgresRDS', config, vpc, rds_sg)

        python_layer = aws_lambda.LayerVersion(self, 
            'py3PostgresLayer',
            code=aws_lambda.Code.from_asset('./sls_fake_ecommerce/database/bootstrap-function/layers/python3_layers.zip'),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_7, aws_lambda.Runtime.PYTHON_3_8],
            description="Python layer for PostgresDB",
            layer_version_name="rds-python3-postgres-layer"
        )

        bootstrap_function = aws_lambda.Function(self, 'postgresBoostrapFunction',
            code=aws_lambda.Code.asset('./sls_fake_ecommerce/database/bootstrap-function/lambda/'),
            function_name="postgres-bootstrap-function",
            handler='bootstrap.lambda_handler',
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            layers=[ python_layer ],
            timeout=core.Duration.minutes(10),
            vpc=vpc,
            security_group=rds_sg
        )

        secret_ssm_policy = aws_iam.PolicyStatement()
        secret_ssm_policy.add_all_resources()
        secret_ssm_policy.add_actions(
            "ssm:Describe*",
            "ssm:Get*",
            "ssm:List*",
            "secretsmanager:GetSecretValue"
        )

        bootstrap_function.add_to_role_policy(secret_ssm_policy)



        provider = cr.Provider(self, "MyProvider",
            on_event_handler=bootstrap_function
        )

        custom_resource = core.CustomResource(self,
            id="customResource",
            service_token=provider.service_token,
            properties={
                "secret_name": "rds-admin-password",
                "region": config['awsRegion']
            }
        )

        custom_resource.node.add_dependency(rds_instance)
        




    