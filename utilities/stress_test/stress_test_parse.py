import os

folder = "rev1_rev2"

DEBUG=False
FREQUENCY=True
TEMPERATURE=True
# Choose to Show or Store the figure
SHOW=False
STORE=True
figureName = "out3.png"

# Keyed entries are for each run, the values of the keys are lists of values
frequency = dict()
temperature = dict()

# Flags for processing control
reading_freq = 0
reading_temp = 0

# Temporary lists
temp_frequencies = list()
temp_temperatures = list()
temp_key = ""

# Loop through every file in the folder
for filename in os.listdir(folder):
    if DEBUG: print("Found file %s"%(filename))
    # Read the file
    with open("%s/%s"%(folder,filename), "r") as fh:
        if DEBUG: print("Reading file %s"%(fh))
        for thisLine in fh:
            if DEBUG: print("Processing line %s"%(thisLine))
            # Start reading the frequencies
            if thisLine.find("frequency") != -1:
                reading_freq = 1
                reading_temp = 0
            # Capture the name
            elif thisLine.find("name") != -1:
                reading_freq = 0
                reading_temp = 0
                temp_key = thisLine.split(":")[1].strip()
            # Start reading the frequencies
            elif thisLine.find("temperature") != -1:
                reading_freq = 0
                reading_temp = 1
            # Reading the data...
            elif thisLine.find("-") != -1:
                if reading_freq == 1:
                    temp_frequencies.append(float(thisLine.strip("- ")))
                elif reading_temp == 1:
                    temp_temperatures.append(float(thisLine.strip("- ")))
            # If not reading data or registering key locations, stop doing anything...
            else:
                reading_freq = 0
                reading_temp = 0
    # When done with the file, store the temp information
    frequency[temp_key] = temp_frequencies
    temperature[temp_key] = temp_temperatures
    temp_frequencies = list()
    temp_temperatures = list()
    temp_key = ""

# Debug
if DEBUG: print(frequency)
if DEBUG: print(temperature)

# Plot
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings; warnings.filterwarnings(action='once')

# Plot Setup
large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'axes.titlesize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large
          }
plt.rcParams.update(params)
if DEBUG: print(plt.style.available)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_style("white")

# Generate an array of colors
# See this page for why the color table was chosen:
#  https://matplotlib.org/stable/users/explain/colors/colormaps.html#qualitative 
#colors = [plt.cm.tab10(i/float(len(frequency.keys())+len(temperature.keys())-1)) for i in range(len(frequency.keys())+len(temperature.keys()))]
colors = [plt.cm.tab20(i/20) for i in range(20)]
if DEBUG: print(colors)

# Plot the data
plt.figure(figsize=(16,10), dpi=80, facecolor='w', edgecolor='k')
plt.grid(which='both', color='gray', linestyle='dotted', linewidth=1)

for i, thisKey in enumerate(temperature.keys()):
    if DEBUG: print("Plotting %s"%(thisKey))
    # Temperature
    if TEMPERATURE: plt.plot(
                [x*10 for x in temperature[thisKey]],
                c=colors[(i*2)%20],
                label="%s [10x C]"%(thisKey)
             )

for i, thisKey in enumerate(frequency.keys()):
    # Frequency
    if FREQUENCY: plt.plot(
                frequency[thisKey],
                c=colors[(i*2+1)%20],
                label="%s [MHz]"%(thisKey)
             )

# Decorations
plt.gca().set(xlabel='Sample')
#plt.gca().set(yscale='log', xlabel='Sample', ylabel='Value')

plt.xticks(fontsize=small); plt.yticks(fontsize=small)
plt.legend(fontsize=small)

# Show Figure
if SHOW: plt.show()

# Save Figure
if STORE: plt.savefig(figureName, bbox_inches='tight')
