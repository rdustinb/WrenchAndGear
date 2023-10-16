#! /bin/bash

# The GitHub repo is here:
# https://github.com/nschloe/stressberry
#
# Need to install stress via apt, and also install stressberry via pip

sudo apt install stress
# Needed to run the test:
pip3 install stressberry
# Needed to create a plot of the results:
pip3 install numpy pandas matplotlib seaborn
