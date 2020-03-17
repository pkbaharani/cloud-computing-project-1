import boto3
import time
from Library import utils
file1=open("test_file",'w+')
file1.write("hello")

#client function
#upload video to the s3, and push key on the sqs
def uploadVideoFile(filename):
    key=filename
    s3_res=boto3.resource('s3')
    #s3_res.meta.client.upload_file(Filename="Saved_Videos/{}".format(filename), Bucket='cse-546-video-files',Key=key)
    s3_res.meta.client.upload_file(Filename="./Library/utils/"+filename, Bucket='cse-546-video-files',Key=key)
    print(key)
    pushSQS(key)

#pushes video key to sqs
#client function
def pushSQS(video_key):
    sqs_name='video-key'
    client = boto3.resource('sqs')
    queue=client.get_queue_by_name(QueueName=sqs_name)
    print(queue.url)
    response = queue.send_message(MessageBody=video_key,MessageAttributes={"Video-Key":{'StringValue':video_key, 'DataType':'String'}})
    print("video key id is : ",response.get('MessageId'))


if __name__=='__main__':
    i=0
    while i in range(7):
        uploadVideoFile("newtestfile")
        i=i+1
        time.sleep(1)
