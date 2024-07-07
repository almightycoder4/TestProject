#!/bin/bash

# Update package list and install dependencies
#apt install sudo
sudo apt-get update
sudo apt-get install -y tesseract-ocr libgl1-mesa-glx python3 python3-pip

# Upgrade pip
python3 -m pip install --upgrade pip

# Install required Python packages
pip3 install virtualenv
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

# Run the Flask application
#python3 run.py
source env/bin/activate