#!/bin/bash

#################################################
# Update and Install some basics that the pi needs...
echo "Updating and upgrading..."
sudo apt update ; sudo apt upgrade -Y

echo "Install git..."
sudo apt install git

echo "Install gvim..."
sudo apt install vim -Y

echo "Install pip..."
sudo apt install python3-pip -Y

echo "Install pyserial via pip..."
pip install pyserial

#################################################
echo "Setting up the terminal and the custom list all scripts..."
mkdir -p ~/bin
cd ~/bin

# Fetch the ps1_coloring script
echo "Fetching the PS1 coloring script..."
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/bin/ps1_coloring

# Fetch the list all script
echo "Fetching the list all script..."
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/bin/list_all.py

# Adding aliases...
echo "Adding aliases..."

echo "alias ll='python3 ~/bin/list_all.py'" >> ~/.bashrc
echo "source bin/ps1_coloring" >> ~/.bashrc

echo "Please logout and back in for changes to take effect."

#################################################
echo "Fetching and running the vim setup script..."
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/setup/vim_setup.sh
chmod +x vim_setup.sh
./vim_setup.sh

#################################################
# First grab the latest version of Docker, and install it
echo "Fetching and installing Docker..."
curl -sSL https://get.docker.com | sh

# Adding the current user to the Docker group so compose files can be run by the user
echo "Adding your username to the docker group..."
sudo usermod -aG docker $$USER

# Fetch the latest docker-compose file...
echo "Fetching the latest docker-compose.yml file..."
cd ~
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/docker/docker-compose.yml
echo "After the reboot, edit the compose file to only include the containers needed to run on this system."
echo "The launch Docker with:"
echo "  docker compose up -d"
echo ""

echo "Rebooting the computer..."
sudo reboot now
