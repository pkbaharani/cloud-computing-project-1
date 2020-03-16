 #!/usr/bin/python3
import record_video
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

sensor = 12
duration = sys.argv[1]

inf = False

if duration == "inf":
    inf = True
else:
    duration = int(duration)
    start_time = datetime.now()
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)

on = 0
off = 0
flag = 0
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
        time.sleep(1)
        end_time = datetime.now()
        if (end_time-start_time).seconds > duration:
            break
    elif i == 1:
        if flag == 0:
            print("Intruder detected")
            on = time.time()
            flag = 1
            print("Recording video")
            record_video.start(10)

            if inf:
                flag = 0
            else:
                end_time = datetime.now()
                if (end_time-start_time).seconds <= duration:
                    flag = 0
        time.sleep(0.1)
        
