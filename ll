
# Code Explanation:
#
# First number ([xx; )
# 38 - signifies we are changing the foreground colors
# 48 - signifies we are changing the background colors
#
# Second number (;xx; )
# 5 - constant for this particular application
#
# Third Number (;xxm )
# This can be one of 257 numbers (0-256), see the
# following script for coloring:
# for fgbg in 38 48 ; do #Foreground/Background
#     for color in {0..256} ; do #Colors
#         #Display the color
#         echo -en "\e[${fgbg};5;${color}m ${color}\t\e[0m"
#         #Display 10 colors per lines
#         if [ $((($color + 1) % 10)) == 0 ] ; then
#             echo #New line
#         fi
#     done
#     echo #New line
# done
# exit 0

DBHEADERCOLOR="\033[38;5;112m"
DBDIRCOLOR="\033[38;5;21m"
DBLINKCOLOR="\033[38;5;164m"
DBENDCOLOR="\033[m"
DBNONECOLOR="\033[38;5;234m"
SINGLEFILE="0"

if [[ -n "$1" ]]
then
    visibledirs=`ls -lhG "$1" | grep "^d" | awk -v DBDIRCOLOR=$DBDIRCOLOR -v DBENDCOLOR=$DBENDCOLOR '{printf("%-11s %3d %6s %s %6s %s %2s %5s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,DBDIRCOLOR$9DBENDCOLOR)}'`
    hiddendirs=`ls -alhG "$1" | grep "^d" | egrep "((;..m\.)|( \.))" | awk -v DBDIRCOLOR=$DBDIRCOLOR -v DBENDCOLOR=$DBENDCOLOR '{printf("%-11s %3d %6s %s %6s %s %2s %5s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,DBDIRCOLOR$9DBENDCOLOR)}'`
    visiblefiles=`ls -lhG "$1" | grep "^-"`
    hiddenfiles=`ls -alhG "$1" | grep "^-" | egrep "((;..m\.)|( \.))"`
    links=`ls -alhG "$1" | grep "^l" | awk -v DBLINKCOLOR=$DBLINKCOLOR -v DBENDCOLOR=$DBENDCOLOR '{printf("%-11s %3d %6s %s %6s %s %2s %5s %s %s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,DBLINKCOLOR$9DBENDCOLOR,$10,$11)}'`
    if [ -f "$1" ]
    then
      SINGLEFILE="1"
    fi
else
    visibledirs=`ls -lhG | grep "^d" | awk -v DBDIRCOLOR=$DBDIRCOLOR -v DBENDCOLOR=$DBENDCOLOR '{printf("%-11s %3d %6s %s %6s %s %2s %5s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,DBDIRCOLOR$9DBENDCOLOR)}'`
    hiddendirs=`ls -ldhG .* | grep "^d" | awk -v DBDIRCOLOR=$DBDIRCOLOR -v DBENDCOLOR=$DBENDCOLOR '{printf("%-11s %3d %6s %s %6s %s %2s %5s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,DBDIRCOLOR$9DBENDCOLOR)}'`
    visiblefiles=`ls -lhG | grep "^-"`
    hiddenfiles=`ls -ldhG .* | grep "^-"`
    links=`ls -alhG | grep "^l" | awk -v DBLINKCOLOR=$DBLINKCOLOR -v DBENDCOLOR=$DBENDCOLOR '{printf("%-11s %3d %6s %s %6s %s %2s %5s %s %s %s\n", $1,$2,$3,$4,$5,$6,$7,$8,DBLINKCOLOR$9DBENDCOLOR,$10,$11)}'`
fi

if [[ "$SINGLEFILE" -eq "0" ]]
then
  if [[ $visibledirs ]]
  then
      echo -e "$DBHEADERCOLOR-------- Directories --------$DBENDCOLOR"
      echo "$visibledirs"
  else
      echo -e "$DBHEADERCOLOR-------- Directories --------$DBENDCOLOR"
      echo -e "$DBNONECOLOR none $DBENDCOLOR"
  fi

  if [[ $hiddendirs ]]
  then
      echo -e "$DBHEADERCOLOR---- Hidden Directories -----$DBENDCOLOR"
      echo "$hiddendirs"
  else
      echo -e "$DBHEADERCOLOR---- Hidden Directories -----$DBENDCOLOR"
      echo -e "$DBNONECOLOR none $DBENDCOLOR"
  fi

  if [[ $visiblefiles ]]
  then
      echo -e "$DBHEADERCOLOR----------- Files -----------$DBENDCOLOR"
      echo "$visiblefiles"
  else
      echo -e "$DBHEADERCOLOR----------- Files -----------$DBENDCOLOR"
      echo -e "$DBNONECOLOR none $DBENDCOLOR"
  fi

  if [[ $hiddenfiles ]]
  then
      echo -e "$DBHEADERCOLOR------- Hidden Files --------$DBENDCOLOR"
      echo "$hiddenfiles"
  else
      echo -e "$DBHEADERCOLOR------- Hidden Files --------$DBENDCOLOR"
      echo -e "$DBNONECOLOR none $DBENDCOLOR"
  fi

  if [[ $links ]]
  then
      echo -e "$DBHEADERCOLOR----------- Links -----------$DBENDCOLOR"
      echo "$links"
  else
      echo -e "$DBHEADERCOLOR----------- Links -----------$DBENDCOLOR"
      echo -e "$DBNONECOLOR none $DBENDCOLOR"
  fi
else
  if [[ $visibledirs ]]
  then
    echo "$visibledirs"
  fi
  if [[ $hiddendirs ]]
  then
    echo "$hiddendirs"
  fi
  if [[ $visiblefiles ]]
  then
    echo "$visiblefiles"
  fi
  if [[ $hiddenfiles ]]
  then
    echo "$hiddenfiles"
  fi
  if [[ $links ]]
  then
    echo "$links"
  fi
fi
