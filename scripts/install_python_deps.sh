#!/bin/bash
set -e

APP_DIR=/home/ubuntu/sysmon-app

# Ownership fix karo pehle
chown -R ubuntu:ubuntu $APP_DIR

cd $APP_DIR

# Purana venv hatao agar exist karta hai
rm -rf venv

# python3-full ensure karo (venv ke liye zaroori hai Ubuntu 24.04 mein)
apt-get install -y python3-full python3-pip

# venv banao ubuntu user ke taraf se
sudo -u ubuntu python3 -m venv venv

# Dependencies install karo
sudo -u ubuntu venv/bin/pip install --upgrade pip
sudo -u ubuntu venv/bin/pip install -r requirements.txt
