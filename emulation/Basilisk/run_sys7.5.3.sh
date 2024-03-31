#!/bin/bash

# Get this Script Location
THISFOLDER=`dirname $0`

# Copy over the system configuration
rsync -av ${THISFOLDER}/Configs/system7.5.3.config ~/.basilisk_ii_prefs

# Run the System
/Applications/BasiliskII.app/Contents/MacOS/BasiliskII &
