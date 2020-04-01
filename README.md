# Cloud Computing Project
## Team Members:
### 1.Prateek Baharani - pbaharan@asu.edu
### 2.Sanchit Pruthi - spruthi@asu.edu
### 3.Siddharth Kumar Nolastname - skuma150@asu.edu


* Setup Details
   - S3 bucket name: cse-546-video-files
      - Input videos path: Input_Videos/
      - Detected output path: Detected_Outputs/

* Prerequisites 
   - On AWS:
      - Access to AWS
      - EC2 worker AMI Id: ami-040ad2e7ebfff6476
   - On Pi:
      - python3
      - python3 libraries on Pi: gc, boto3, psutil, tracemalloc, picamera

* Execution instructions
   - On AWS:
       - Log into the Autoscalar EC2 instance
       - Run the command “python3 ~/auto-scale/controller/cloud-computing-project-1/manager.py”
   - On Pi:
       - Copy all contents of “darknet” directory into “cloud-computing-project-1” (a.k.a. Project folder)
       - Create directories: “Input_Videos/” and “Detected_Outputs/” in “cloud-computing-project-1”
       - Copy AWS Provided AWS credentials to “~/.aws/credentials” on “Pi” and “AutoScaler” (EC2 instance).
       - Disable display on Pi: Run “Xvfb :1 & export DISPLAY=:1”
       - Cd to “cloud-computing-project-1”
       - Run “init_script.sh <no_of_videos> <video_length_secs>“ on Raspberry Pi. 
       - Darkent results are pushed to Amazon S3 bucket “cse-546-video-files” inside directory “Detected_Outputs/”
