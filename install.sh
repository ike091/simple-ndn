#!/bin/bash

# this bash script installs various NDN software

sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:named-data/ppa -y
sudo apt-get update

sudo apt-get install nfd -y
sudo apt-get install ndn-tools -y
sudo apt-get install ndn-traffic-generator -y
sudo apt-get install nslr -y
sudo apt-get install libchronosync -y
sudo apt-get install libpsync -y

mkdir -p ~/nlsr/log/

mv /local/repository/nlsr.conf ~/nlsr/
