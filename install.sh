#!/bin/bash

# this script installs the NDN forwarding daemon

sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:named-data/ppa -y
sudo apt-get update

sudo apt-get install nfd -y
sudo apt-get install ndn-tools -y
