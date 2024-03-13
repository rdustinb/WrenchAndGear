#!/bin/bash

# Change the default shell
chsh -s /bin/bash

# Create the needed .bash_profile file to source the .bashrc file from
echo "source ~/.bashrc" >> ~/.bash_profile

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

#################################################
# Install WGet and MacVIM
echo "Using brew to install wget and macvim..."
brew install wget
brew install macvim

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

#################################################
echo "Fetching and running the vim setup script..."
cd ~
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/setup/vim_setup.sh
chmod +x vim_setup.sh
./vim_setup.sh
rm vim_setup.sh

#################################################
# First grab the latest version of Docker, and install it
echo "Fetching and installing Docker..."
brew install docker

# Fetch the latest docker-compose file...
echo "Fetching the latest docker-compose.yml file..."
cd ~
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/docker/docker-compose.yml
echo "After the reboot, edit the compose file to only include the containers needed to run on this system."
echo "The launch Docker with:"
echo "  docker compose up -d"
echo ""

echo "Please install the custom font 'Source Code Pro for Powerline.otf' located in the $HOME directory."
echo "Please reboot for changes to take effect..."

#################################################
# Install Tart for running VMs
# This replaces the older use of Vagrant + VirtualBox since they no longer support the m-series Apple Silicon
echo "Fetching and installing Tart for virtualizing..."
brew install cirruslabs/cli/tart

#################################################
# Automate VM Creation with Packer
echo "Fetching and installing Packer for VM automation..."
brew tap hashicorp/tap
brew install hashicorp/tap/packer

#################################################
# Setup Syntax Highlighting for HCL
mkdir -p ~/.vim/pack/jvirtanen/start
cd ~/.vim/pack/jvirtanen/start
git clone https://github.com/jvirtanen/vim-hcl.git
