#!/bin/bash
set -e

# Copy sysmon.service to systemd
cp /home/ubuntu/sysmon-app/sysmon.service /etc/systemd/system/

# Reload and start service
systemctl daemon-reload
systemctl enable sysmon
systemctl restart sysmon
