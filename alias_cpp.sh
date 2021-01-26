#!/bin/bash

DIRCPPSCRIPT=$(dirname -- "$BASH_SOURCE") > /dev/null

alias cppclang="clang++ -Werror -Wextra -Wall -std=c++98 *.cpp"
alias cppclass="python3 $DIRCPPSCRIPT/class.py"
alias cppupdate="python3 $DIRCPPSCRIPT/update.py"