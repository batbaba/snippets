import boto3
import traceback

region = "eu-west-1"


def lambda_handler(event, context):
    stsClient = boto3.client("sts")
    testList = [
        # {"id": "343610773987"},
        # {"id": "408031766763"},
        # {"id": "485091988892"},
        {"id": "495678590846"},
    ]  # Koen #Iman #Dieter #Mergen
    for account in testList:
        print("".join(["arn:aws:iam::", account["id"], ":role/AllowEC2Shutdown"]))

        stsResponse = stsClient.assume_role(
            DurationSeconds=3600,
            RoleArn="".join(["arn:aws:iam::", account["id"], ":role/AllowEC2Shutdown"]),
            RoleSessionName="shutdownLambda",
        )

        ACCESS_KEY = stsResponse["Credentials"]["AccessKeyId"]
        SECRET_KEY = stsResponse["Credentials"]["SecretAccessKey"]
        SESSION_TOKEN = stsResponse["Credentials"]["SessionToken"]

        # shutdownEC2(ACCESS_KEY, SECRET_KEY, SESSION_TOKEN)
        # shutdownASG(ACCESS_KEY, SECRET_KEY, SESSION_TOKEN)
        shutdownRDS(ACCESS_KEY, SECRET_KEY, SESSION_TOKEN)
    return "success"


def shutdownRDS(ACCESS_KEY, SECRET_KEY, SESSION_TOKEN):
    rdsClient = boto3.client(
        "rds",
        region_name=region,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )

    allRds = rdsClient.describe_db_instances()
    allInstances = set()
    keepOnList = set()
    # print(allRds)
    try:
        for rds in allRds["DBInstances"]:
            rdsTags = rdsClient.list_tags_for_resource(
                ResourceName=rds["DBInstanceArn"]
            )
            # print(
            #     rdsClient.stop_db_instance(
            #         DBInstanceIdentifier=rds["DBInstanceIdentifier"]
            #     )
            # )
    except Exception:
        print("RDS error:")
        traceback.print_exc()


def shutdownASG(ACCESS_KEY, SECRET_KEY, SESSION_TOKEN):
    asgClient = boto3.client(
        "autoscaling",
        region_name=region,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    allAsg = asgClient.describe_auto_scaling_groups()
    try:
        for asg in allAsg["AutoScalingGroups"]:
            print(asg["AutoScalingGroupName"])
            asgClient.update_auto_scaling_group(
                AutoScalingGroupName=asg["AutoScalingGroupName"],
                MaxSize=0,
                MinSize=0,
                DesiredCapacity=0,
            )
    except Exception:
        print("ASG error:")
        traceback.print_exc()


def shutdownEC2(ACCESS_KEY, SECRET_KEY, SESSION_TOKEN):
    ec2 = boto3.client(
        "ec2",
        region_name=region,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    instanceDict = ec2.describe_instances()
    # print(instanceDict)
    allInstances = set()
    keepOnList = set()
    try:
        for instances in instanceDict["Reservations"]:
            for instance in instances["Instances"]:
                try:
                    allInstances.add(instance["InstanceId"])
                    for tag in instance["Tags"]:
                        if (
                            "shutdownInstance" in tag.values()
                            and "false" in tag.values()
                        ):
                            keepOnList.add(instance["InstanceId"])
                except Exception:
                    # print("EC2 error:")
                    # traceback.print_exc()
                    pass

        shutdownInstances = allInstances - keepOnList
        # print(allInstances)
        print("ec2.stop_instances(InstanceIds=(list((shutdownInstances))))")
    except Exception:
        print("EC2 error:")
        traceback.print_exc()
        pass


lambda_handler("", "")
