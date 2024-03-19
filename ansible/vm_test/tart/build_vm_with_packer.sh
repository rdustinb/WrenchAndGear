#!/bin/bash

# Remove the old VM ssh keys
ssh-keygen -R "debian-vm.local"

# Delete the original VM if it is present
tart delete debian-12.5.0-vanilla

# This uses the Packer tool to generate a vanilla VM with a Packer build file:
packer build -var-file variables.pkrvars.hcl build_debianOS.pkr.hcl

# Start the VM
tart run debian-12.5.0-vanilla &

sleep 15

# Copy the ssh keys over to the new VM
thisUsername=`grep username variables.pkrvars.hcl | awk '{print $3}' | sed -e 's/"//g'`
# TODO this requires user intervention, which sucks...
ssh-copy-id ${thisUsername}@debian-vm.local
