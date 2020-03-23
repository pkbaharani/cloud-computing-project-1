import boto3
from botocore.exceptions import ClientError
from ec2_metadata import ec2_metadata

INSTANCE_STATE="Instance_State/{}"

def start_darknet(videokey):
    #initiating darknet code here
    pass


def get_my_instance_id():
    return ec2_metadata.instance_id
    #print(myInstanceId)


def update_instance_state(instanceid,value):
    key=INSTANCE_STATE.format(instanceid)
    s3_res=boto3.client('s3')
    s3_res.put_object(Body=str(value), Bucket='cse-546-video-files',Key=key)


def get_instance_state(instanceid):
    s3 = boto3.resource('s3')
    key=INSTANCE_STATE.format(instanceid)
    obj = s3.Object('cse-546-video-files',key)
    body = obj.get()['Body'].read()
    return int(body)

def start_instnace(instanceid):
    print('starting new instance -',instanceid)
    try:
        ec2 = boto3.client('ec2')
        response = ec2.start_instances(InstanceIds=[instanceid], DryRun=False)
        print(response)
        update_instance_state(instanceid,1) # setting value for this instance as one in s3 bucket.
    except ClientError as e:
        print(e)


def stop_instance(instanceid):
    try:
        ec2 = boto3.client('ec2')
        response = ec2.stop_instances(InstanceIds=[instanceid], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)


'''
#****************NOT REQUIRED ****************
#create new ec2-instance on request
def create_instance():
    print("creating instance")
    ec2 = boto3.resource('ec2')
    instance = ec2.create_instances(
    ImageId = 'ami-009d6802948d06e52',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.micro',
    KeyName = 'cc-ec2-manager')
    instanceIds[(instance[0].id)]=1
'''
