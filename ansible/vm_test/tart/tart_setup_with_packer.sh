#!/bin/bash

# This uses the Packer tool to generate a vanilla VM with a Packer build file:
packer build -var-file variables.pkrvars.hcl init.pkr.hcl
