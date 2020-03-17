import boto3
from botocore.exceptions import ClientError
from ec2_metadata import ec2_metadata

#concern: sync between manager and worker while flapping the state bit



def get_my_instance_id():
    return ec2_metadata.instance_id
    #print(myInstanceId)

def get_instance_id():
    #write code to parse ec2metadata and get instance id
    instanceid=""
    pass

def update_instance_state(instanceid,value):

    s3_res=boto3.client('s3')
    s3_res.put_object(Body=str(value), Bucket='instance-state',Key=instanceid)

def get_instance_state(instanceid):
    s3 = boto3.resource('s3')
    obj = s3.Object('instance-state',instanceid)
    body = obj.get()['Body'].read()
    return int(body)

def stop_instance():
    try:
        ec2 = boto3.client('ec2')
        response = ec2.stop_instances(InstanceIds=[instanceid], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)


#download video file from the s3 // this function should be in EC-2
def getVideoFile(object_name):
    s3 = boto3.client('s3')
    print(object_name)
    s3.download_file('cse-546-video-files',object_name, object_name)


#polling key from the sqs
def get_video_key():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='video-key')
    print("getting messages")
    que=queue.receive_messages(MessageAttributeNames=['Video-Key'])
    if len(que)>0:
        #start_instnace()

        video_key = ''
        print('in for loop')

        message=que[0]
        if message.message_attributes is not None:
             video_key = message.message_attributes.get('Video-Key').get('StringValue')

        print('video key is ',video_key,'end')
        message.delete()
        return video_key
    else:
        update_instance_state(instanceid,0) #instance is going to shut down


def start_darknet(videokey):
    #initiating darknet code here
    pass

def push_result_s3(filename):
    key=filename
    s3_res=boto3.resource('s3')
    #s3_res.meta.client.upload_file(Filename=<path_to_saved_result>.format(filename), Bucket='cse-546-video-darknet-results',Key=key)
    s3_res.meta.client.upload_file(Filename="./Library/utils/"+filename, Bucket='cse-546-video-darknet-results',Key=key)

if __name__=='__main__':

    flag=1
    instanceid=get_my_instance_id()
    #state=get_instance_state(instanceid)
    while(flag):
        videokey=get_video_key()
        if videokey is not None:
            print(videokey)
            #create_instance()
            #getVideoFile function call has to be put in Ec2
            getVideoFile(videokey)
            start_darknet(videokey)
            push_result_s3("newtestfile") # for this file name which is the output file specify the format
            
        flag=get_instance_state(instanceid)
    stop_instance()
