#!/bin/sh

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

echo "${green}Install some Developer Tools...${reset}"
sudo apt-get -y install build-essential git cmake pkg-config

echo "${green}Install Image packages...${reset}"
sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

echo "${green}Install Video packages...${reset}"
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev

echo "${green}Install GTK...${reset}"
sudo apt-get -y install libgtk2.0-dev

echo "${green}Install optimization packages...${reset}"
sudo apt-get -y install libatlas-base-dev gfortran

echo "${green}Install python headers...${reset}"
sudo apt-get -y install python2.7-dev python3-dev

echo "${green}Grab OpenCV 3.3.0 code...${reset}"
cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/3.3.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
unzip opencv_contrib.zip

echo "${green}Compile and install OpenCV 3.3.0...${reset}"
cd ~/opencv-3.3.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=ON \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
	-D BUILD_EXAMPLES=ON ..
make -j4
sudo make install
sudo ldconfig