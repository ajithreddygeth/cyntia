import os.path


from aws_cdk import (
    aws_ec2 as ec2,
    App, Stack
)

from constructs import Construct

dirname = os.path.dirname(__file__)


class VPC(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC
        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=3,
                           vpc_name="",
                           cidr="10.10.0.0/16",
                           # configuration will create 3 groups in 3 AZs = 9 subnets.
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="Public",
                               cidr_mask=21
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                               name="Private",
                               cidr_mask=21
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                               name="DB",
                               cidr_mask=21
                           )
                           ],
                           nat_gateways=2,
                           # gateway_endpoints={
                           #          "S3": ec2.GatewayVpcEndpointOptions(
                           #              service=ec2.GatewayVpcEndpointAwsService.S3
                           #          )
                           #      }
                           )
    # # Private endpoint to use AWS backbone to pull ECR images 
    #         # Need ECR, ECR-API , S3 to use the backbone svc # https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html
    #         self.vpc.add_interface_endpoint("EcrDockerEndpoint",
    #                                         service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER)
    #         self.vpc.add_interface_endpoint("EcrEndpoint", 
    #                                         service=ec2.InterfaceVpcEndpointAwsService.ECR)

app = App()
VPC(app, "VPC")

app.synth()
