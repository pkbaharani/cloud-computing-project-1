import boto3
import time
import Library.sqs  as SQS
"""file1=open("../test_file", 'rw+')
file1.write("hello")
file1.close()"""

S3_BUCKET="cse-546-video-files"
INPUT_S3_FOLDER = "Input_Videos/{}"
OUTPUT_S3 = "Detected_Outputs/{}"


def upload_file(file_path, bucket_name, key):
    s3_res=boto3.resource('s3', region_name="us-east-1")
    s3_res.meta.client.upload_file(Filename=file_path, Bucket=bucket_name,
                                   Key=key)

#client function
#upload video to the s3, and push key on the sqs
def uploadVideoFile(file_path):
    filename = file_path.split("/")[-1]
    s3_key = INPUT_S3_FOLDER.format(filename)
    upload_file(file_path, S3_BUCKET, s3_key)
    print("Uploaded {} to S3 bucket".format(filename))
    SQS.pushSQS(s3_key)
    print("Pushed key to S3 bucket")
    return


def upload_output_file(file_path):
    filename = file_path.split("/")[-1]
    upload_file(file_path, S3_BUCKET, OUTPUT_S3.format(filename))
    print("Uploaded output file {}".format(filename))
    return
    
    
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
