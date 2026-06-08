#!/bin/bash
set -e

APP_DIR="/home/ubuntu/sysmon-app"

# Fix ownership of app directory
sudo chown -R ubuntu:ubuntu $APP_DIR

cd $APP_DIR

# Delete existing venv before recreating
rm -rf venv

# Create venv using sudo -u ubuntu
sudo -u ubuntu python3 -m venv venv

# Install requirements using venv pip
sudo -u ubuntu venv/bin/pip install --upgrade pip
sudo -u ubuntu venv/bin/pip install -r requirements.txt
