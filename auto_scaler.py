import boto3
from botocore.exceptions import ClientError
from ec2_metadata import ec2_metadata

MAX_EC2_INSTANCES = 10

def start_instnace(instanceid):
    try:
        ec2 = boto3.client('ec2')
        response = ec2.start_instances(InstanceIds=[instanceid], DryRun=False)
    except ClientError as e:
        print(e)


def process_ec2_machines():
  sqs = boto3.client('sqs')
  queue = sqs.get_queue_by_name(QueueName='video-key')

  que=queue.receive_messages(MessageAttributeNames=['Video-Key'])
  que_length=int(queue.attributes.get('ApproximateNumberOfMessages'))

  if que_length > 0:
    # Get list of stopped and running instances
    ec2 = boto3.resource('ec2')
    running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    stopped_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    
    for inst in running_instances:
      print("Running: ", inst.id, instance.instance_type)
    
    for inst in stopped_instances:
      print("Stopped: ", inst.id, instance.instance_type)

process_ec2_machines()

