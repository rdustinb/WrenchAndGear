#!/bin/bash

# Before shutting down the DNS server, pull the latest Pihole Image
docker pull pihole/pihole

# Now stop the currently running Pihole container
docker stop pihole

# Remove the old container (this will not remove the local content)
docker rm -f pihole

# Now launch the new container
docker compose up -d

# Done!
