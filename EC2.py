import boto3
from botocore.exceptions import ClientError
from ec2_metadata import ec2_metadata
import Library.ec2Interface as EC2i
import Library.sqs as SQS
import Library.s3 as S3
import sys
import detect_objects as do
#concern: sync between manager and worker while flapping the state bit

if __name__=='__main__':
    flag=1
    typ=sys.argv[1]

    instanceid=EC2i.get_my_instance_id()
    #state=get_instance_state(instanceid)
    while(flag):
        videokey=SQS.get_video_key()
        if videokey is None:            # if the queue is empty, simply update the state in s3 and stop this instance
            break
        print(videokey)
        S3.getVideoFile(videokey)
        do.start(videokey)
        #import pdb;pdb.set_trace()
        #EC2i.start_darknet(videokey)
        #S3.push_result_s3("newtestfile") # for this file name which is the output file specify the format
        print('darknet done here........')
        #S3.upload_output_file(videokey)
        #EC2i.start_darknet(videokey)
        #S3.upload_output_file()
        flag=SQS.get_video_key()

        #flag=EC2i.get_instance_state(instanceid)
    if typ!='test':
        EC2i.update_instance_state(instanceid,0)
        EC2i.stop_instance(instanceid)
