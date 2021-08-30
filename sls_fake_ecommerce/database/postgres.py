from typing import Dict, List

from aws_cdk import (
    aws_rds as rds,
    core,
    aws_ec2 as ec2
)

class PostgresRds(core.Construct):

    def __init__(self, scope: core.Construct, id: str, config: Dict, vpc: ec2.Vpc, rds_postgres: ec2.SecurityGroup) -> None:
        super().__init__(scope, id)
        
        self.config = config
        self.vpc = vpc
        self.__create_rds_instance()

    def __create_rds_instance(self):
        rds.DatabaseInstance(
            scope=self, 
            id="RDS",
            database_name="ecommercedb",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_13_3
            ),
            # vpc=ec2.Vpc.from_vpc_attributes(
            #     id=self.vpc.vpc_id,
            #     scope=self
            # ),
            vpc=self.vpc,
            vpc_subnets={
                "subnet_type": ec2.SubnetType.PRIVATE
            },
            port=5432,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            allocated_storage=20,
            max_allocated_storage=30,
            credentials=rds.Credentials.from_generated_secret("postgres"),
            publicly_accessible=False
        )