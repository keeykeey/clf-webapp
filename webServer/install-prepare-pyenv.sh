#! bin/bash

sudo yum -y update
sudo yum install python36-devel -y
mkdir clf-webapp
python3 -m venv clf-webapp
source clf-webapp/bin/activate


pip install --upgrade pip
pip install flask==1.1.1
