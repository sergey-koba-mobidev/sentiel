#!/bin/sh

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

echo "${green}Cloning the project...${reset}"
sudo apt-get -y install git
git clone https://github.com/sergey-koba-mobidev/sentinel.git
cd sentinel

echo "${green}Installing packages...${reset}"
sudo apt-get -y install libjpeg-dev
pip install boto3
pip install pyyaml
pip install Pillow
sudo python3 -m pip install pyyaml # for server.py

echo "${green}Create default config...${reset}"
touch config.yml