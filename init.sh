#!/bin/bash
# install.sh for client(rpi)
apt-get --yes install python3
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs #install nodejs
apt-get --yes install npm # install npm

npm install caver-js #if it is not working, how about try -g option?

pip install ino

python3 setting.py

exit 0
