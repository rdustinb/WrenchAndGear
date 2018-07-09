#!/local/myapps/bin/python3

"""
  The purpose of this script is to alias a quick command to list all of the files and folders
  in the current directory or in a specified directory as passed by argument, and separate them
  by type and then organize them alphabetically and by size.

  The format will be:
    Directories
    Hidden Directories
    Files
    Hidden Files
    Links
"""

import subprocess
import sys

try:
  specifiedFolder = ''.join(sys.argv[1])
except:
  specifiedFolder = "."

thisDir = subprocess.check_output("ls -alh "+specifiedFolder, universal_newlines=True, shell=True).split("\n")[1:-1]
whoAmI = subprocess.check_output("whoami", universal_newlines=True, shell=True).strip()

theseHiddenDirs = list()
theseDirs = list()
theseHiddenFiles = list()
theseFiles = list()
theseLinks = list()

allStuffs = list()

fieldZeroMax  = 0
fieldOneMax   = 0
fieldTwoMax   = 0
fieldThreeMax = 0
fieldFourMax  = 0
fieldSixMax   = 0
fieldSevenMax = 0

# For coloring codes check out these sites:
#   https://misc.flogisoft.com/bash/tip_colors_and_formatting
#   https://unix.stackexchange.com/questions/124407/what-color-codes-can-i-use-in-my-ps1-prompt
colorSectionLabels = "38;5;172"
colorMyUsername = "1;38;5;150"
colorTypeFolders = "38;5;25"
colorTypeFiles = "38;5;251"
colorTypeLinkSymbol = "38;5;163"
colorNones = "38;5;240"
colorSizeMega = "38;5;202"
colorSizeGiga = "38;5;9"
colorFlagsGroupBgd = "48;5;237"
colorFlagsGroupNoneBgd = "48;5;237m\033[30"
colorFlagsUserBgd = "48;5;239"
colorFlagsUserNoneBgd = "48;5;239m\033[30"

def getMaxFields(line):
  global fieldZeroMax
  global fieldOneMax
  global fieldTwoMax
  global fieldThreeMax
  global fieldFourMax
  global fieldSixMax
  global fieldSevenMax
  # Standardize the field size outputs
  if len(line.split()[0]) > fieldZeroMax:  fieldZeroMax  = len(line.split()[0])
  if len(line.split()[1]) > fieldOneMax:   fieldOneMax   = len(line.split()[1])
  if len(line.split()[2]) > fieldTwoMax:   fieldTwoMax   = len(line.split()[2])
  if len(line.split()[3]) > fieldThreeMax: fieldThreeMax = len(line.split()[3])
  if len(line.split()[4]) > fieldFourMax:  fieldFourMax  = len(line.split()[4])
  if len(line.split()[6]) > fieldSixMax:   fieldSixMax   = len(line.split()[6])
  if len(line.split()[7]) > fieldSevenMax: fieldSevenMax = len(line.split()[7])

def alignFields(line):
  global colorNones
  global colorSizeMega
  global colorSizeGiga
  fields = line.split()[0][1:]
  newFields = ""
  for i in range(len(fields)):
    if   i >= 0 and i < 3 and fields[i] == "-": newFields = newFields+colored(fields[i], colorFlagsUserNoneBgd)
    elif i >= 0 and i < 3 and fields[i] != "-": newFields = newFields+colored(fields[i], colorFlagsUserBgd)
    elif i >= 3 and i < 6 and fields[i] == "-": newFields = newFields+colored(fields[i], colorFlagsGroupNoneBgd)
    elif i >= 3 and i < 6 and fields[i] != "-": newFields = newFields+colored(fields[i], colorFlagsGroupBgd)
    else: newFields = newFields+fields[i].replace("-", colored("-", colorNones)).replace(".", colored(".", colorNones))
  part0 = newFields + \
    " "*(fieldZeroMax-len(line.split()[0])) + " "*(fieldOneMax-len(line.split()[1])+1) + line.split()[1] + \
    " " + line.split()[2].replace(whoAmI, colored(whoAmI, colorMyUsername)) + \
    " "*(fieldTwoMax-len(line.split()[2])+1) + line.split()[3] + \
    " "*(fieldThreeMax-len(line.split()[3])+1) + " "*(fieldFourMax-len(line.split()[4])) + \
    line.split()[4].replace("M", colored("M", colorSizeMega)).replace("G", colored("G", colorSizeGiga)) + \
    " " + line.split()[5] + \
    " "*(fieldSixMax-len(line.split()[6])+1) + line.split()[6] + \
    " "*(fieldSevenMax-len(line.split()[7])+1) + line.split()[7]
  part1 = ' '.join(line.split()[8:])
  if len(part1.split("->")) > 1 :
    part1,part3 = part1.split(" -> ",1)
    part2 = "->"
    return part0,part1,part2,part3
  else:
    return part0,part1

for line in thisDir:
  if   line[0] == 'd' and line.split()[8][0] == '.':
    # Hidden Folder
    theseHiddenDirs.append(line)
    getMaxFields(line)
  elif line[0] == 'd' and line.split()[8][0] != '.':
    # Visible Folder
    theseDirs.append(line)
    getMaxFields(line)
  elif line[0] == '-' and line.split()[8][0] == '.':
    # Hidden Files
    theseHiddenFiles.append(line)
    getMaxFields(line)
  elif line[0] == '-' and line.split()[8][0] != '.':
    # Visible Files
    theseFiles.append(line)
    getMaxFields(line)
  elif line[0] == 'l' :
    theseLinks.append(line)
    getMaxFields(line)

def colored(thisString, thisColor):
  return '\033[%sm%s\033[0m'%(thisColor,thisString)

print(colored("-------- Directories --------", colorSectionLabels))
for line in theseDirs:
  # We need to pad certain fields with spaces so everything lines up pretty-like
  part0,part1 = alignFields(line)
  print("%s %s" % (part0,colored(part1, colorTypeFolders)) )
if not theseDirs:
  print(colored("None", colorNones))

print(colored("----- Hidden Directories ----", colorSectionLabels))
for line in theseHiddenDirs:
  part0,part1 = alignFields(line)
  print("%s %s" % (part0,colored(part1, colorTypeFolders)) )
if not theseHiddenDirs:
  print(colored("None", colorNones))

print(colored("----------- Files -----------", colorSectionLabels))
for line in theseFiles:
  part0,part1 = alignFields(line)
  print("%s %s" % (part0,colored(part1, colorTypeFiles)) )
if not theseFiles:
  print(colored("None", colorNones))

print(colored("-------- Hidden Files -------", colorSectionLabels))
for line in theseHiddenFiles:
  part0,part1 = alignFields(line)
  print("%s %s" % (part0,colored(part1, colorTypeFiles)) )
if not theseHiddenFiles:
  print(colored("None", colorNones))

print(colored("----------- Links -----------", colorSectionLabels))
for line in theseLinks:
  part0,part1,part2,part3 = alignFields(line)
  print("%s %s %s %s" % (part0,colored(part1, colorTypeFiles),colored(part2, colorTypeLinkSymbol),colored(part3, colorNones)) )
if not theseLinks:
  print(colored("None", colorNones))