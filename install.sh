#!/bin/bash
# install.sh for client(rpi)
apt-get --yes install python3
apt-get --yes install node # install node 
apt-get --yes install npm # install npm

npm install -g caver-js

apt-get --yes install arduino
pip install arduino-sketch

python3 setting.py

exit 0
