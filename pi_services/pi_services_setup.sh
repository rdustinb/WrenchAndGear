#!/bin/bash

# First grab the latest version of Docker, and install it
echo "Fetching and installing Docker..."
curl -sSL https://get.docker.com | sh

# Adding the current user to the Docker group so compose files can be run by the user
echo "Adding your username to the docker group..."
sudo usermod -aG docker dustin

# Fetch the latest docker-compose file...
echo "Fetching the latest docker-compose.yml file..."
cd ~
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/pi_services/docker-compose.yml
echo "After the reboot, edit the compose file to only include the containers needed to run on this system."
echo "The launch Docker with:"
echo "  docker compose up -d"
echo ""

echo "Rebooting the computer..."
sudo reboot now
