#!/bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install wget curl lsb-release -y
sudo apt install python3 python3-pip -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb || sudo apt install -f -y
git clone https://github.com/deno4908/Mediafire_TOOL
cd Mediafire_TOOL
pip install -r requirements.txt --break-system-packages --force-reinstall --ignore-installed
python3 run.py
