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
            database_name=self.config['data']['rds']['dbname'],
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_13_3
            ),
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
            credentials=rds.Credentials.from_username(
                username=self.config['data']['rds']['dbadmin'],
                exclude_characters='"@/\\;"',
                secret_name="rds-admin-password"
            ),
            publicly_accessible=False,
            iam_authentication=True,
            backup_retention=core.Duration.days(3),
        ).connections.allow_internally(ec2.Port.all_tcp(), 'All traffic within SG')