#!/bin/bash

fullpath="$1"

# Get the variable configurations
source config.sh

# Working NAS
scp "$fullpath" $username@$hostname:$primaryDrive/

# Backup Drive
scp "$fullpath" $username@$hostname:$backupDrive/
