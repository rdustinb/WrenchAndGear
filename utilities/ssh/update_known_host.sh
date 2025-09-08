#!/bin/bash

# Get the command line arguments, -h and -u are REQUIRED
for i in "$@"
do
case $i in
    -h=*|--hostname=*)
    thisHost="${i#*=}"
    ;;
    -u=*|--username=*)
    thisUser="${i#*=}"
    ;;

    *)
    echo "./update_known_host.sh -h HOSTNAME -u USERNAME"
    exit 1
    ;;
esac
done

# Check that username and hostname are both set
if [ -z ${thisHost} ]; then
  echo "./update_known_host.sh -h HOSTNAME -u USERNAME"
  exit 1
fi

if [ -z ${thisUser} ]; then
  echo "./update_known_host.sh -h HOSTNAME -u USERNAME"
  exit 1
fi

# Remove the current known hostname
ssh-keygen -R $thisHost

# Copy the key to the host once again
ssh-copy-id $thisUser@$thisHost
