#!/bin/bash

COLORON="\033[38;5;112m"
COLOROFF="\033[m"

if [ -z "$1" ]
then
  echo -e "\n${COLORON}---------- Directories ----------${COLOROFF}"
  if gls -al | egrep -q "^d"; then
    gls --color=always -al | egrep "^d"
  else
    echo "None"
  fi
  echo -e "\n${COLORON}------------- Files -------------${COLOROFF}"
  if gls -al | egrep -q "^-"; then
    gls --color=always -al | egrep "^-"
  else
    echo "None"
  fi
  echo -e "\n${COLORON}------------- Links -------------${COLOROFF}"
  if gls -al | egrep -q "^l"; then
    gls --color=always -al | egrep "^l"
  else
    echo "None"
  fi
else
  echo -e "\n${COLORON}---------- Directories ----------${COLOROFF}"
  if gls -al "$1" | egrep -q "^d"; then
    gls --color=always -al "$1" | egrep "^d"
  else
    echo "None"
  fi
  echo -e "\n${COLORON}------------- Files -------------${COLOROFF}"
  if gls -al "$1" | egrep -q "^-"; then
    gls --color=always -al "$1" | egrep "^-"
  else
    echo "None"
  fi
  echo -e "\n${COLORON}------------- Links -------------${COLOROFF}"
  if gls -al "$1" | egrep -q "^l"; then
    gls --color=always -al "$1" | egrep "^l"
  else
    echo "None"
  fi
fi

