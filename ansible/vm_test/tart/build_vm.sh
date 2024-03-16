#!/bin/bash

# Tart Quick Start:
# https://tart.run/quick-start/

# For a full list of available VM images, go here:
# https://github.com/orgs/cirruslabs/packages?repo_name=linux-image-templates

# Using predefined VM Configs:
tart clone ghcr.io/cirruslabs/debian:latest debian
tart set debian --cpu       2
tart set debian --memory    4096
tart run debian

