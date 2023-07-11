#!/bin/bash

cd ~

mkdir -p ~/bin

cd ~/bin

# Fetch the ps1_coloring script
echo "Fetching the PS1 coloring script..."
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/bin/ps1_coloring

# Fetch the list all script
echo "Fetching the list all script..."
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/bin/list_all.py

cd ~

# Adding aliases...
echo "Adding aliases..."

echo "alias ll='python3 ~/bin/list_all.py'" >> .bashrc
echo "source bin/ps1_coloring" >> .bashrc

echo "Please logout and back in for changes to take effect."
