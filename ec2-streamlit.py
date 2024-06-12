# ec2-streamlit.py is a python script that accompanies the AWS Workshop Use Generative AI to Build a DevSecOps Chatbot

import boto3
import time
import sys
import json

model_name = sys.argv[1]

ec2 = boto3.client("ec2")
iam = boto3.client("iam")
kendra = boto3.client("kendra")
s3 = boto3.client('s3')
sts = boto3.client('sts')

# Pull account number and store it as a variable
account_id = sts.get_caller_identity().get('Account')

# Create IAM Role and Policy
print('Setting up the right permissions')
assume_role_doc = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole",
        }
    ],
}

policy_doc = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kendra:*",
                "bedrock:*",
                "s3:*"
            ],
            "Resource": "*",
        }
    ],
}

policy_name = "gen-ai-policy-" + str(time.time()).split('.')[0]
pol_response = iam.create_policy(
    PolicyName=policy_name, PolicyDocument=json.dumps(policy_doc)
)
policy_arn = pol_response["Policy"]["Arn"]
role_name = "gen-ai-role-" + str(time.time()).split('.')[0]
iam.create_role(
    RoleName=role_name, AssumeRolePolicyDocument=json.dumps(assume_role_doc)
)
iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
profile_name = "gen-ai-profile-" + str(time.time()).split('.')[0]
profile_response = iam.create_instance_profile(InstanceProfileName=profile_name)

time.sleep(10)
profile_arn = profile_response["InstanceProfile"]["Arn"]

iam.add_role_to_instance_profile(
    InstanceProfileName=profile_name, RoleName=role_name
)

# Look up Kendra Index and print Kendra Index ID
print('looking up kendra index...')
kendra_index_id = kendra.list_indices()['IndexConfigurationSummaryItems'][0][
    'Id'
]
print (kendra_index_id)

# Lookup VPC and print VPC ID
print('finding default vpc...')

vpc_id = ec2.describe_vpcs(
     Filters=[{"Name": "is-default", "Values": ["true"]}],
)['Vpcs'][0]['VpcId']

print (vpc_id)

# Create Security Group
print('creating security group...')
sec_group = ec2.create_security_group(
    Description='stremlit security group',
    GroupName='streamlit-sg' + str(time.time()),
    VpcId=vpc_id,
)
sec_group_id = sec_group['GroupId']

authorize = ec2.authorize_security_group_ingress(
    GroupId=sec_group_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 8501,
            'ToPort': 8501,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
        }
    ],
)

# Create EC2 Instance
print('creating instance...')
instance = ec2.run_instances(
    ImageId="ami-0efcece6bed30fd98",
    MinCount=1,
    MaxCount=1,
    InstanceType="t3.medium",
    SecurityGroupIds=[
        sec_group_id,
    ],
    IamInstanceProfile={'Name': profile_name},
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'streamlit-boto3'},
            ],
        },
    ],
    UserData=f'''#!/bin/bash -xe
export DEBIAN_FRONTEND=noninteractive 
apt update
apt install awscli python3-pip python3-venv unzip -y
aws s3 cp s3://genai-devsecops-chatbot-{account_id}/generative-ai-to-build-a-devsecops-chatbot.zip .
unzip generative-ai-to-build-a-devsecops-chatbot.zip
cd generative-ai-to-build-a-devsecops-chatbot
python3 -m venv .venv
source .venv/bin/activate
pip3 install boto3 langchain streamlit
pip3 install -U langchain-community
export AWS_REGION=us-west-2
export KENDRA_INDEX_ID={kendra_index_id}
streamlit run app.py {model_name}
''',
)

public_ip = None

try:
    instance_id = instance.get('Instances')[0].get('InstanceId')
    describe = ec2.describe_instances(
        InstanceIds=[
            instance_id,
        ],
    )
    public_ip = (
        describe.get('Reservations')[0]
        .get('Instances')[0]
        .get('PublicIpAddress')
    )
except:
    pass

while public_ip is None:
    print('waiting for public ip...')
    time.sleep(10)
    describe = ec2.describe_instances(
        InstanceIds=[
            instance_id,
        ],
    )
    public_ip = (
        describe.get('Reservations')[0]
        .get('Instances')[0]
        .get('PublicIpAddress')
    )

# Print Streamlit App URL
print('')
print('*** Your streamlit app will be available in a few minutes at: ***')
print('')
print(f"http://{public_ip}:8501")
