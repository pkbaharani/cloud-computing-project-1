#!/bin/bash
mkdir cronjobworking
Xvfb :1 & export DISPLAY=:1
#sleep(1)
cd ~/worker/cloud-computing-project-1
python3 ./EC2.py prod
