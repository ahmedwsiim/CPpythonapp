#!/bin/bash
cd /home/ubuntu/sysmon-app
source venv/bin/activate
nohup python3 main.py > app.log 2>&1 &
