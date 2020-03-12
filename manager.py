import boto3

instanceIds={}

#Manager monitors queue and creates new instance if there is an element
#We need to split this function i.e for Manager: do {monitor queue and create instace } and for EC2 do {get message from the queue}
def monitorQueue():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='video-key')
    print("getting messages")
    que=queue.receive_messages(MessageAttributeNames=['Video-Key'])
    if len(que)>0:
        video_key = ''
        print('in for loop')

        message=que[0]
        if message.message_attributes is not None:
             video_key = message.message_attributes.get('Video-Key').get('StringValue')

        print('video key is ',video_key,'end')
        message.delete()
        return video_key

#download video file from the s3 // this function should be in EC-2
def getVideoFile(object_name):
    s3 = boto3.client('s3')
    print(object_name)
    s3.download_file('cse-546-video-files',object_name, object_name)

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


