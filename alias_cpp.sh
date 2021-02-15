#!/bin/bash

if [ -n $BASH_SOURCE -a ! "$BASH_SOURCE" = "" ];then
	DIRCPPSCRIPT=$(dirname -- "$BASH_SOURCE") > /dev/null
else
	DIRCPPSCRIPT=$(dirname -- "$0") > /dev/null
fi

alias clangall="clang++ -Werror -Wextra -Wall -std=c++98 *.cpp"
alias cppclass="python3 $DIRCPPSCRIPT/class.py"
alias cppupdate="python3 $DIRCPPSCRIPT/update.py"