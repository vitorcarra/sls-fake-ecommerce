from aws_cdk import (
    aws_rds as rds,
    aws_ec2 as ec2,
    core,
)

class DataStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id)

        vpc = ec2.Vpc(self, "VPC")

        rds.DatabaseInstance(
            self, "RDS",
            database_name="ecommerce-db",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_13_3
            ),
            vpc=vpc,
            port=5432,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.NANO,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
        ),