#!/bin/bash

# Get the file to copy
echo "What file do you want to store remotely?"
read thisFile

# Get the variable configurations
source config.sh

# Working NAS
scp "$thisFile" $username@$hostname:$primaryDrive

# Backup Drive
scp "$thisFile" $username@$hostname:$backupDrive
