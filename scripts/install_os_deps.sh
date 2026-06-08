#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

# Remove apt/dpkg locks
rm -f /var/lib/apt/lists/lock
rm -f /var/cache/apt/archives/lock
rm -f /var/lib/dpkg/lock
rm -f /var/lib/dpkg/lock-frontend
dpkg --configure -a || true

apt-get update
apt-get install -y python3 python3-pip python3-full python3-venv
