#pushes video key to sqs
#client function
import boto3

SQS_NAME = 'video-key'
def pushSQS(video_key):
    client = boto3.resource('sqs', region_name="us-east-1")
    queue=client.get_queue_by_name(QueueName=SQS_NAME)
    print(queue.url)
    response = queue.send_message(MessageBody=video_key,MessageAttributes={"Video-Key":{'StringValue':video_key, 'DataType':'String'}})
    print("video key id is : ",response.get('MessageId'))

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
