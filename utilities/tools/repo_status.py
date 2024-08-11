from pathlib import Path
import subprocess
import sys

path = str(sys.argv[1])

# Use to store the results of the function
gitFolders = []

# Function to recursively find all folders containing a ".git"
def findGits(thisDir):
    try:
        # Get the items in this folder
        for thisNextDir in Path(thisDir).iterdir():
            # Only work with directories
            if thisNextDir.is_dir():
                thisNextDir = str(thisNextDir)
                # Is this is a .git directory, append it and stop recursing
                if thisNextDir.find(".git") != -1:
                    gitFolders.append(thisNextDir.strip(".git"))
                    continue
                else:
                    findGits(thisNextDir)
    except PermissionError:
        None

# Recusively find the .git folders
if __name__ == '__main__':
    findGits(path)

    for thisFolder in gitFolders:
        print("\n%s"%(thisFolder))
        subprocess.call(['git', 'status', thisFolder])
