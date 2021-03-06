# Rebuild the PATH
PATH=''
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
PATH=$PATH:~/Documents/bin

# Aliases
if [ -z ${gvim+blah} ]
then
  alias gvim=/Users/${USER}/Documents/bin/mvim
  export gvim
fi

if [ -z ${sr+blah} ]
then
  alias sr='source ~/.bashrc'
fi

# Change the PS1 Variable
function exitstatus {
  EXITSTATUS="$?"

  BOLD="\[\033[1m\]"
  OFF="\[\033[m\]"

  GOOD="${BOLD}\[\033[38;5;19m\]"
  BAD="${BOLD}\[\033[38;5;52m\]"

  GRAYMED="\[\033[38;5;252m\]"
  AMPERSAND="\[\033[38;5;172m\]"
  GRAYDARK="\[\033[38;5;238m\]"

  COMMONPROMPT1="\n${GRAYDARK}\w${OFF}\n"
  COMMONPROMPT2=" [${BOLD}\u${OFF}${AMPERSAND}@${OFF}${GRAYMED}\h${OFF}] $ "

  if [ "${EXITSTATUS}" -eq 0 ]
  then
    # Good Last Command
    PS1="${COMMONPROMPT1}${GOOD}:)${OFF}${COMMONPROMPT2}"
  else
    # Bad Last Command
    PS1="${COMMONPROMPT1}${BAD}:X${OFF}${COMMONPROMPT2}"
  fi
}
PROMPT_COMMAND=exitstatus
