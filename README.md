# WrenchAndGear
This repository will contain configuration settings for tools I use so that I may tweak them in one place and have those configurations available everywhere.

## Raspberry Pi Setup
Run this command on the Raspberry Pi to set it up the way I like it:

``` bash
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/setup/pi_setup.sh ; chmod +x pi_setup.sh ; ./pi_setup.sh
```

## Launch Script
This script is used to parse the SpaceFlight Insider [Launch Calendar](http://www.spaceflightinsider.com/launch-schedule/) and properly format the event fields, writing them via the Google Calendar API to my Google Calendar. You can us it too, you just need to modify the script to point to YOUR Google Calendar API Instance and the calendars Public URL.

## .vimrc Configuration
My configuration of VIM uses **Pathogen** for package installation.

My configuration uses either **Source Code Pro for Powerline** (MacOSX), or **Liberation Mono for Powerline** (Linux) for development.

[Powerline Fonts](https://github.com/powerline/fonts)

My configuration also requires the **codeschool** colorscheme.

I use these tools, see the setup script for information:
 * vim-airline
 * vim-airline-themes
 * vim-gitgutter
 * vim-indent-guides
 * nerdtree
 * tabular
 * vim-colorschemes
 * verilog_systemverilog
 * vim-visual-increment
