#!/bin/bash

diskutil list

echo "Which disk to unmount and copy? If the disk is /dev/disk4, just enter 'disk4':"
read thisDisk

echo "What is the name of the file to recover?"
read thisFile

sudo diskutil unmountDisk /dev/$thisDisk

ddrescue -r3 /dev/$thisDisk $thisFile.img $thisFile.log
