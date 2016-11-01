# Critical Commands
This scratchpad note will hold critical commands that I have found useful during
my coding adventures.

Terminal
---
```
egrep -il "  " ./* -A 0
```

  * &lt;CTRL&gt;+v, &lt;TAB&gt; will add a tab between the quotes allowing searching for tab spaces in all files in a directory.

VIM
---


Pebble Development
---


FPGA Development
---

Mac Environment
---
Meld for OSX can be downloaded here:
https://yousseb.github.io/meld/

Edit the .gitconfig file with these sections:
```
[diff]
  tool = meld
[difftool]
  prompt = false
[difftool "meld"]
  trustExitCode = true
  cmd = open -W -a Meld --args \"$LOCAL\" \"$PWD/$REMOTE\"
[merge]
  tool = meld
[mergetool]
  prompt = false
[mergetool "meld"]
  trustExitCode = true
  cmd = open -W -a Meld --args --auto-merge \"$PWD/$LOCAL\" \"$PWD/$BASE\" \"$PWD/$REMOTE\" --output=\"$PWD/$MERGED\"
```

This will allow meld to be used as gitdiff

---
iCloud setup on the Mac has become extremely bloated, so if there is a small drive being utilized it might be best to disable all iCloud "sync" features except those directly used on the Mac in question. For instance, disabling the following freed up almost 5GB:

* Photos
* Mail

```
rm -fr ~/Library/Mail/V3
```

* Calendar
* Reminders
* Safari
* Keychain
* Back to My Mac

```
defaults -currentHost write com.apple.ImageCapture disableHotPlug -bool true
```

  * This will disable Apple's _Auto Open_ feature when any device is plugged in.

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

  * Install the missing package manager _Homebrew_ on Mac OSX.

#### Disk Space Savings
```
defaults write com.apple.iTunes DeviceBackupsDisabled -bool true
```

  * Disable iTunes from backing up any iDevices. Can save a lot of space.

```
defaults write com.apple.Safari DebugSnapshotsUpdatePolicy -int 2
```

  * Tell Safari to not store Top Sites and not save Cover Flow icons.

```
sudo rm /private/var/vm/s*
```

  * Deletes the SwapFile
  * Deletes the Sleep Image created when the Mac Hybernates

```
brew update;
brew upgrade;
brew cleanup
```

  * Deletes the old cached archives in ~/Library/Caches/Homebrew
  * The currently-installed packages will remain (**\*.bottle.tar.gz**)

```
sudo rm -fr /Library/Caches/CrashPlan/*
```

  * Removes all the locally cached crap from CrashPlan. These are uneeded and will be regenerated if needed.

[Download Monolingual](https://github.com/IngmarStein/Monolingual/releases/download/v1.7.3/Monolingual-1.7.3.dmg)

Total savings of disk space seen is about 300MB.

```
cd /System/Library/Speech/Voices/ ; sudo find . ! -name 'Vicki.SpeechVoice' -type d -exec rm -fr {} +
```

  * Removes all voice synthesizers except Vicki.
  * Total Savings of nearl 3.5GB

<pre>
cd /Library/Dictionaries ; sudo find . \
! 'Apple Dictionary.dictionary' \
! -name 'New Oxford American Dictionary.dictionary' \
! -name 'French - English.dictionary' \
! -name 'Oxford American Writer's Thesaurus.dictionary' \
! -name 'German - English.dictionary' \
! -name 'Spanish - English.dictionary' \
-type d -exec rm -fr {} +
</pre>

  * Remove unused Dictionaries
  * Of the few I have saved here, there are a couple that are not on by default in the Dictionaries App.

```
FontBook
```
  * Pruning through All Fonts, removing a lot of the foreign languages will free up about ~600MB

