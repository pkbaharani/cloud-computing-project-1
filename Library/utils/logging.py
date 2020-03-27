import time

class logging:


    file_handler=None
    def __init__(self):
        self.file_handler()


    def file_handler(self):
        filename="logs/ec2-logs"+str(int(time.time()))
        file=open(filename,'a+')
        self.file_handler=file


    def log_it(self,event):
        timestamp=self.get_time_stamp()
        event=timestamp+" : "+event
        self.file_handler.write(event)


    def get_time_stamp(self):
        localtime=time.localtime()
        timestamp=time.asctime(localtime)
        return str(timestamp)

