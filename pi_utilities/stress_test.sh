#! /bin/bash

# This will run tests from 1-4 cores
cd ~
mkdir stress_test
cd stress_test

# 1 Core
stressberry-run -n '1 Core' -c 1 core1.dat

# Let things cool off...
sleep 5m

# 2 Core
stressberry-run -n '2 Core' -c 2 core2.dat

# Let things cool off...
sleep 5m

# 3 Core
stressberry-run -n '3 Core' -c 3 core3.dat

# Let things cool off...
sleep 5m

# 4 Core
stressberry-run -n '4 Core' -c 4 core4.dat

echo -e "\n\nStress test done!\n\n"
