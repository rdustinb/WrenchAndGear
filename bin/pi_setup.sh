#!/bin/bash

cd ~

# Update and Install some basics that the pi needs...
echo "Updating and upgrading..."
sudo apt update ; sudo apt upgrade -Y

echo "Install git..."
sudo apt install git

echo "Install gim..."
sudo apt install vim

echo "Fetching and running the bin setup script..."
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/bin/bin_setup.sh
chmod +x bin_setup.sh
./bin_setup.sh

echo "Fetching and running the vim setup script..."
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/env_and_vim/vim_setup.sh
chmod +x vim_setup.sh
./vim_setup.sh

echo "Rebooting..."
sudo reboot now
