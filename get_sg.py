import boto3
import traceback
import csv
import json
import random

# ------------- get all security groups
ec2_client = boto3.client("ec2")
all_sg = ec2_client.describe_security_groups()


def lambda_handler():
    sg_name="boto3_test_sg"+str(random.randint(1, 100))
    new_sg = create_sg(sg_name,sg_name, "vpc-0ad9c797b609b985d")
    new_sg_add_rules = sg_add_rules(new_sg["GroupId"], "sg-06eaebf0fc12ca83b")


# ------------- create SG
def create_sg(sg_name, sg_description, vpc_id):
    new_sg = ec2_client.create_security_group(
        Description=sg_description, GroupName=sg_name, VpcId=vpc_id, DryRun=False
    )
    return new_sg


def sg_add_rules(new_sg_name, source_sg_name):
    # ------------- copy existing sg
    ec2_resource = boto3.resource("ec2")
    source_security_group = ec2_resource.SecurityGroup(source_sg_name)
    source_sg_rules = source_security_group.ip_permissions

    # ------------- new sg
    new_sg_resource = ec2_resource.SecurityGroup(new_sg_name)
    for sg_rule in source_sg_rules:
        cidr_ranges = sg_rule["IpRanges"]
        port_range = sg_rule["FromPort"]
        protocol = sg_rule["IpProtocol"]
        try:
            new_sg_resource.authorize_ingress(
                GroupId=new_sg_name,
                IpPermissions=[
                    {
                        "FromPort": int(port_range),
                        "ToPort": int(port_range),
                        "IpProtocol": protocol,
                        "IpRanges": cidr_ranges,
                    }
                ],
            )
        except Exception as e:
            print(e)


lambda_handler()
