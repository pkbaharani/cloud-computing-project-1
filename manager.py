import boto3
from botocore.exceptions import ClientError
from time import time
instanceIds={}

#Manager monitors queue and creates new instance if there is an element
#We need to split this function i.e for Manager: do {monitor queue and create instace } and for EC2 do {get message from the queue}
def monitorQueue():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='video-key')
    print("getting messages")
    que=queue.receive_messages(MessageAttributeNames=['Video-Key'])
    if len(que)>0:
        start_instnace()

        video_key = ''
        print('in for loop')

        message=que[0]
        if message.message_attributes is not None:
             video_key = message.message_attributes.get('Video-Key').get('StringValue')

        print('video key is ',video_key,'end')
        message.delete()
        return video_key



def auto_scale():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='video-key')
    print("getting messages")
    que=queue.receive_messages(MessageAttributeNames=['Video-Key'])
    que_length=len(que)

    #shut all the instances if there is nothing in the queue
    if que_length==0:
        for instance in instanceIds:
            update_instance_state(instance,0)
        return

    #check if number of running instance > the size of the queue, downscale is required
    #if que_length in range (15):

    upcount=0;
    for instance in instanceIds:
        temp=get_instance_state(instance)
        upcount=upcount+temp

    if upcount == 15: # 15 is the total number of instances available out of 20 resources
        #downscale
        if que_length<upcount:
            for i in range(que_length,upcount+1):
                instance=instanceIds[i]
                update_instance_state(instance,0)
                return
    #upscale
    if upcount<15 and upcount<que_length:
        diff=min(que_length-upcount,15-upcount) # this is to reach maximum capacity or to empty the queue
        for i in range (15):
            if(diff==0):
                break

            temp=get_instance_state(i)
            if temp == 0:
                intance=instanceIds[i]
                start_instnace(instance)    # starting instance
                update_instance_state(instance,1) # updating the state in s3
                diff=diff-1


def get_instance_ids():
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        print (instance.id , instance.state)
        # write code, do not add the managers instance id
        instanceIds[instance.id]=0

def start_next_available_instance():

    for instanceid in instanceIds:
        if instanceIds[instanceid]==0:
            start_instnace(instanceid)

def update_instance_state(instanceid,value):

    s3_res=boto3.client('s3')
    s3_res.put_object(Body=str(value), Bucket='instance-state',Key=instanceid)


def get_instance_state(instanceid):
    s3 = boto3.resource('s3')
    obj = s3.Object('instance-state',instanceid)
    body = obj.get()['Body'].read()
    return int(body)

def start_instnace(instanceid):

    try:
        ec2 = boto3.client('ec2')
        response = ec2.start_instances(InstanceIds=[instanceid], DryRun=False)
        print(response)
        update_instance_state(instanceid,1) # setting value for this instance as one in s3 bucket.
    except ClientError as e:
        print(e)




#NOT REQUIRED
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

#get_instance_state("blablabla")

if __name__=='__main__':
    get_instance_ids()
    while True:
        auto_scale()
        time.sleep(30)


'''
if __name__=='__main__':
    i=0
    while True:
        videokey=monitorQueue()
        if videokey is not  None:
            print(videokey)
            create_instance()
             # getVideoFile function call has to be put in Ec2
            getVideoFile(videokey)
        print(instanceIds)
        print(i)
        i=i+1


'''
