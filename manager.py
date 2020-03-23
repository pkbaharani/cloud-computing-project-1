import boto3
from botocore.exceptions import ClientError
from ec2_metadata import ec2_metadata
import Library.sqs as SQS
import Library.ec2Interface as EC2i
import time

instanceIds=[]
instanceCount=0
myInstanceId=''

def auto_scale():
    que_length=SQS.get_queue_length()
    print('queue length is ',que_length)

    #CASE-1 -> shut all the instances if there is nothing in the queue
    if que_length==0:
        shut_all_instances()
        return

    upcount=get_total_ec2_upcount()     #get count of the number of instances that are up

    #Case-2 -> upscale
    if upcount<instanceCount and upcount<que_length:
        upscale(que_length,upcount)

    #Case-3 -> check if downscale is required
    if upcount == instanceCount: # 15 is the total number of instances available out of 20 resources
        if que_length<upcount:
            # CASE-2-> downscale
            downscale(que_length,upcount)


def shut_all_instances():
    for instance in instanceIds:
            EC2i.update_instance_state(instance,0)


def upscale(que_length,upcount):
    diff=min(que_length-upcount,instanceCount-upcount) # this is to reach maximum capacity or to empty the queue
    for i in range(instanceCount):
        if(diff==0):
            break
        print(instanceIds)
        print('\n\n\n\n value of i-----------> ', i,'   and instnace id is ',instanceIds[i],'\n\n\n\n')
        temp=EC2i.get_instance_state(instanceIds[i])
        print('value of temp is ',temp)
        if temp == 0:
            instance=instanceIds[i]
            EC2i.start_instnace(instance)                   # starting instance
            EC2i.update_instance_state(instance,1)          # updating the state in s3
            diff=diff-1


def downscale(que_length,upcount):
    for i in range(que_length,upcount+1):
        instance=instanceIds[i]
        EC2i.update_instance_state(instance,0)
        return


def get_total_ec2_upcount():
    upcount=0;
    for instance in instanceIds:
        temp=EC2i.get_instance_state(instance)
        upcount=upcount+temp
    return upcount


def get_instance_ids():
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        print (instance.id , instance.state)
        myinstanceid=EC2i.get_my_instance_id()
        if myinstanceid!=instance.id:
            instanceIds.append(instance.id)


if __name__=='__main__':

    #start-up sequence
    get_instance_ids()
    instanceCount=len(instanceIds)
    print(instanceCount)
    print(instanceIds)

    #initialize the state of all the ec2 instances to off in s3
    for instance in instanceIds:
        EC2i.update_instance_state(instance,0)
#    time.sleep(60)
    while True:
        auto_scale()
        time.sleep(30)



'''
#******NOT REQUIRED at this time *************
def start_next_available_instance():

    for instanceid in instanceIds:
        if instanceIds[instanceid]==0:
            EC2i.start_instnace(instanceid)



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
