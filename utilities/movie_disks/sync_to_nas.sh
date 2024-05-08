#!/bin/bash

fullpath="$1"

# Get the variable configurations
source config.ini
echo "Username: $username"
echo "Primary Drive syncing to: $primaryDrive"
echo "Secondary Drive syncing to: $backupDrive"

# Working NAS
scp "$fullpath" $username@$hostname:$primaryDrive/

# Backup Drive
scp "$fullpath" $username@$hostname:$backupDrive/
