 #!/usr/bin/python3
import pi_utils
import detect_objects
from multiprocessing import Pool
import Library.s3 as S3
import psutil

'''
SETUP:

    -   -->     GND     -->     PIN6
    +   -->     5V      -->     PIN4
    S   -->     GPIO18  -->     PIN12

'''

import RPi.GPIO as GPIO
import subprocess
import time
import sys
from datetime import datetime
import tracemalloc
import gc
import threading

sensor = 12
video_count = sys.argv[1]
record_time = int(sys.argv[2])

inf = False

if video_count == "inf":
    video_count = 9223372036854775807
else:
    video_count = int(video_count)
start_time = datetime.now()
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)

on = 0
off = 0
flag = 0
current_count = 0
#pi_utils.set_free()

tracemalloc.start()
while flag == 0:
    i=GPIO.input(sensor)
    if i == 0:
        if flag == 1:
            off = time.time()
            diff = off - on
            print('time: ' + str(diff%60) + ' sec')
            print('')
            flag = 0
        print("No intruders")
        if not pi_utils.is_busy:	
                darknet_thread2 = threading.Thread(target=detect_objects.get_from_SQS_and_start)
                darknet_thread2.start()
        time.sleep(1)
        if current_count > video_count:
            break
    elif i == 1:
        if flag == 0:
            current_count += 1
            print("Intruder detected")
            on = time.time()
            flag = 1
            print("Recording video")
            file_path = pi_utils.record_video(record_time)
            time.sleep(0.1)  
            gc.collect()
            if pi_utils.is_busy():
                #pool = Pool(processes=2)
                #result2 = pool.apply_async(S3.uploadVideoFile, [file_path])
                #S3.uploadVideoFile(file_path)
                video_thread = threading.Thread(target=S3.uploadVideoFile, args=(file_path,))
                video_thread.start()
            else:
                #pi_utils.set_busy()
                darknet_thread = threading.Thread(target=detect_objects.start, args=(file_path,))
                darknet_thread.start()
                #pool = Pool(processes=2)
                #result = pool.apply_async(detect_objects.start, [file_path, True])
                #detect_objects.start(file_path)
                
                #detect_objects.start(file_path)
                #result.get()
                #pool.close()
                #pool.join()
            if inf:
                flag = 0
            else:
                if current_count < video_count:
                    flag = 0
        time.sleep(0.1)

while pi_utils.is_busy() or detect_objects.get_from_SQS_and_start() != None:
    continue
        
