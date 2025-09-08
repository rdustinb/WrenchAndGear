from pathlib import Path
import subprocess
import sys
# This is probably installed in a venv...
import git

colorError = "38;5;150"
colorWarning = "38;5;172"
colorNone = "38;5;240"

# Get the path to search for repos
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
                if thisNextDir.endswith('.git'):
                    gitFolders.append(thisNextDir.replace('.git', ''))
                    continue
                else:
                    findGits(thisNextDir)
    except PermissionError:
        None

# This colors text printed to the terminal
def colored(thisString, thisColor):
  return '\033[%sm%s\033[0m'%(thisColor,thisString)

# Recusively find the .git folders
if __name__ == '__main__':
    findGits(path)

    for thisFolder in gitFolders:
        print("\n%s"%(thisFolder))
        my_repo = git.Repo(thisFolder)
        # Check for local modifications
        if my_repo.is_dirty():
            print(colored("Local modifications.", colorError))
        else:
            print(colored("No local modifications.", colorNone))
        # Check for untracked files
        if my_repo.is_dirty(untracked_files=True):
            print(colored("Untracked files.", colorWarning))
        else:
            print(colored("No untracked files.", colorNone))
