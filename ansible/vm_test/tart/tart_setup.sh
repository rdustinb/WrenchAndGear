#!/bin/bash

# Tart Quick Start:
# https://tart.run/quick-start/

# For a full list of available VM images, go here:
# https://github.com/orgs/cirruslabs/packages?repo_name=linux-image-templates

# Using predefined VM Configs:
#tart clone ghcr.io/cirruslabs/debian:latest debian
#tart run debian

# Create my Own VM
tart create --linux --disk-size 20 Debian
tart set --cpu        2            Debian
tart set --memory     4096         Debian

# Install the OS
tart run --disk debian-12.5.0-arm64-DVD-1.iso:ro Debian
# <ENTER> 4x times to start install with default location and keyboard.
# Wait 20s
# -vm.local to append to the default "debian" hostname
# Wait 5s
# @str0n0my!<ENTER> to create the root password
# @str0n0my!<ENTER> to confirm the root password
# sudood<ENTER> to create the user's name
# <ENTER> to use the same for the username
# @str0n0my!<ENTER> to create the user's password
# @str0n0my!<ENTER> to confirm the user's password
# M<ENTER> to select Mountain time
# Wait 5s
# <ENTER> to select Guided Partition disks
# SS<ENTER> to select the Separate /home, /var, and /tmp partitions
# Wait 5s
# <ENTER> to finish partitioner
# Wait 5s
# <TAB><ENTER> to partition disks
# Wait 20s
# <TAB><TAB><ENTER> to use a network mirror
# <ENTER><ENTER><ENTER> to finish setting up the network mirror
# Wait 10s
# <ENTER> to skip using popularity contest

# Run the VM after the OS is installed
tart run Debian
