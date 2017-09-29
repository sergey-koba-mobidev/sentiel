#!/bin/sh

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

echo "${green}Cloning the project...${reset}"
apt-get -y install git
git clone https://github.com/sergey-koba-mobidev/sentinel.git
cd sentinel

printf "${green}Installing packages...${reset}"
apt-get -y install libjpeg-dev
pip install boto3
pip install pyyaml
pip install Pillow

printf "${green}Create default config...${reset}"
touch config.yml