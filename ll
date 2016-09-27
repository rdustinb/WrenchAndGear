
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
DBENDCOLOR="\033[m"
DBNONECOLOR="\033[38;5;234m"

if [[ -n "$1" ]]
then
    first=`gls -alh --color=always "$1" | grep "^d"`
    second=`gls -alh --color=always "$1" | grep "^-"`
    third=`gls -alh --color=always "$1" | grep "^l"`
else
    first=`gls -alh --color=always | grep '^d'`
    second=`gls -alh --color=always | grep '^-'`
    third=`gls -alh --color=always | grep '^l'`
fi

if [[ $first ]]
then
    echo -e "$DBHEADERCOLOR-------- Directories --------$DBENDCOLOR"
    echo "$first"
else
    echo -e "$DBHEADERCOLOR-------- Directories --------$DBENDCOLOR"
    echo -e "$DBNONECOLOR none $DBENDCOLOR"
fi

if [[ $second ]]
then
    echo -e "$DBHEADERCOLOR----------- Files -----------$DBENDCOLOR"
    echo "$second"
else
    echo -e "$DBHEADERCOLOR----------- Files -----------$DBENDCOLOR"
    echo -e "$DBNONECOLOR none $DBENDCOLOR"
fi

if [[ $third ]]
then
    echo -e "$DBHEADERCOLOR----------- Links -----------$DBENDCOLOR"
    echo "$third"
else
    echo -e "$DBHEADERCOLOR----------- Links -----------$DBENDCOLOR"
    echo -e "$DBNONECOLOR none $DBENDCOLOR"
fi
