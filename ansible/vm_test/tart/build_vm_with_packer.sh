#!/bin/bash

# Delete the original VM if it is present
tart delete debian-12.5.0-vanilla

# This uses the Packer tool to generate a vanilla VM with a Packer build file:
packer build -var-file variables.pkrvars.hcl build_debianOS.pkr.hcl
