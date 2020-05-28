#!/bin/bash

# this bash script installs various NDN software

# set up ppa repository
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:named-data/ppa -y
sudo apt-get update

# install ndn software
sudo apt-get install nfd -y
sudo apt-get install ndn-tools -y
sudo apt-get install ndn-traffic-generator -y
sudo apt-get install nlsr -y
sudo apt-get install libchronosync -y
sudo apt-get install libpsync -y

# create a directory for nlsr logging
mkdir -p ~/nlsr/log/

# copy the nlsr configuration file to the nlsr directory
cp /local/repository/nlsr.conf ~/nlsr/

# copy my .vimrc on each VM (I really like my remappings)
cp /local/repository/.vimrc ~/
