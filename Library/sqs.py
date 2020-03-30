#pushes video key to sqs
#client function
import boto3

SQS_NAME = 'video-key'


def get_queue_length():
    sqs = boto3.resource('sqs', region_name="us-east-1")
    queue = sqs.get_queue_by_name(QueueName='video-key')
    print("getting queue length")
    return int(queue.attributes.get('ApproximateNumberOfMessages'))
    #que=queue.receive_messages(MessageAttributeNames=['Video-Key'])

def pushSQS(video_key):
    client = boto3.resource('sqs', region_name="us-east-1")
    queue=client.get_queue_by_name(QueueName=SQS_NAME)
    print(queue.url)
    response = queue.send_message(MessageBody=video_key,MessageAttributes={"Video-Key":{'StringValue':video_key, 'DataType':'String'}})
    print("video key id is : ",response.get('MessageId'))

#polling key from the sqs
def get_video_key():
    sqs = boto3.resource('sqs', region_name="us-east-1")
    queue = sqs.get_queue_by_name(QueueName='video-key')
    print("getting messages")
    que=queue.receive_messages(MessageAttributeNames=['Video-Key'])
    que_length=get_queue_length()
    if que_length>0:
        #start_instnace()
        video_key = ''
        message=que[0]
        if message.message_attributes is not None:
             video_key = message.message_attributes.get('Video-Key').get('StringValue')

        print('video key is ',video_key,'end')
        message.delete()
        return video_key
    else:
        return None
        #update_instance_state(instanceid,0) #instance is going to shut down


'''
#*********NOT Required**************
#Manager monitors queue and creates new instance if there is an element
#We need to split this function i.e for Manager: do {monitor queue and create instace } and for EC2 do {get message from the queue}

#this function is not required at this point
def monitorQueue():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='video-key')
    print("getting messages")
    que=queue.receive_messages(MessageAttributeNames=['Video-Key'])
    if len(que)>0:
        EC2i.start_instnace()

        video_key = ''
        print('in for loop')

        message=que[0]
        if message.message_attributes is not None:
             video_key = message.message_attributes.get('Video-Key').get('StringValue')

        print('video key is ',video_key,'end')
        message.delete()
        return video_key

'''
