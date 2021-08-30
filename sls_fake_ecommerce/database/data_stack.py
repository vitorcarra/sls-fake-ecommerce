from typing import Dict
from aws_cdk import (
    aws_rds as rds,
    aws_ec2 as ec2,
    core,
)

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

        rds = PostgresRds(self, 'PostgresRDS', config, vpc, rds_sg)


    