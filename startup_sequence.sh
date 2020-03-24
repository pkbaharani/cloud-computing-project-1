#!/bin/bash

Xvfb :1 & export DISPLAY=:1
#sleep(1)
bash get-aws-cred
cd ~/worker/cloud-computing-project-1
python3 ./EC2.py prod
