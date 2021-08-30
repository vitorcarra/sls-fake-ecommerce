from aws_cdk import (
    core,
    aws_ec2 as ec2
)


class SecurityGourp(core.Construct):
    _vpc: ec2.Vpc
    rds_sg: ec2.SecurityGroup

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc) -> None:
        super().__init__(scope, id)

        self._vpc = vpc
        self.__create_rds_sg()

    # Create elasticsearch security group
    def __create_rds_sg(self) -> ec2.SecurityGroup:
        self.rds_sg = ec2.SecurityGroup(
            self, 'RDSPostgres',
            security_group_name='RdsPostgresSg',
            vpc=self._vpc,
            description='Postgres security group',
        )