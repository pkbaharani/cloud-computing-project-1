import boto3
import time
file1=open("../test_file", 'rw+')
file1.write("hello")

#client function
#upload video to the s3, and push key on the sqs
def uploadVideoFile(filename):
    keyy="test_file"+str(int(time.time()))
    s3_res=boto3.resource('s3')
    s3_res.meta.client.upload_file(Filename="../test_file", Bucket='cse-546-video-files',
                                   Key=keyy)
    print(keyy)
    pushSQS(keyy)

#manager function

def create_instance():
    print("creating instance")
    ec2 = boto3.resource('ec2')
    instance = ec2.create_instances(
    ImageId = 'ami-009d6802948d06e52',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.micro',
    KeyName = 'cc-ec2-manager')
    print("here..")
    print('Your newly created instance id is :',instance[0].id)

def monitorQueue():
    sqs = boto3.resource('sqs')


#pushes video key to sqs
#client function
def pushSQS(video_key):
    sqs_name='video-key'
    client = boto3.resource('sqs')
    queue=client.get_queue_by_name(QueueName=sqs_name)
    print(queue.url)
    response = queue.send_message(MessageBody=video_key,MessageAttributes={"Video-Key":{'StringValue':video_key, 'DataType':'String'}})
    print("video key id is : ",response.get('MessageId'))


if __name__ == '__main__':
    print("hello")
    for i in range(10):
        uploadVideoFile()
    #create_instance()
    #client=boto3.client('ec2',region_name='us-east-1')
    #resp=client.run_instances(ImageId='ami-0903fd482d7208724',InstanceType='t2.micro',MinCount=1,MaxCount=3)
    #ec2=boto3.resource('ec2')
    #instance=ec2.Instance(image_id='ami-0903fd482d7208724')


    #import boto3


   #SubnetId = 'subnet-0yhg678990d56c277') print (instance[0].id)
'''
old function
def pushSQS(video_key):
    sqs_name='video-key'
    client = boto3.resource('sqs')
    queue=client.get_queue_by_name(QueueName=sqs_name)
    print(queue.url)
    response = queue.send_message(MessageBody=video_key)
    print("video key id is : ",response.get('MessageId'))

'''

'''
old function
def monitorQueue():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='video-key')
    print("getting messages")
    for message in queue.receive_messages(MessageAttributeNames=['Video-Key']):
        video_key = ''
        print('in for loop')
        if message.message_attributes is not None:
            video_key = message.message_attributes.get('Video-Key').get('StringValue')
        print('video key is ',video_key,'end')
        message.delete()
        return video_key


'''
