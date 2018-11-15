#!/bin/bash
# install.sh for client(rpi)

apt-get --yes install node # install node 
apt-get --yes install npm # install npm
npm install -g caver-js

apt-get --yes install arduino

exit 0
