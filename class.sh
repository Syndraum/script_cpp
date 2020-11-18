#!/bin/bash

function	checkFileExist {
	if [ -f $1 ];then
		echo "File $1 already exist"
		exit 1
	fi
	return 0
}

function	setClass {
	printf "#include \"$hpp\"\n\n$className::$className()\n{\n\t\n}\n\n$className::~$className()\n{\n\t\n}\n" > $cpp
}

function	setHeader {
	nameUpper=$(echo $name | tr a-z A-Z)
	printf "#ifndef $nameUpper\n#define $nameUpper\n\nclass $className\n{\n\tpublic:\n\n\t$className();\n\t~$className();\n};\n\n#endif\n" > $hpp
}

# 			createClass([-c], name, ...)
function	createClass {
	if [ -z "$1" ];then
		echo "Need name of one class"
		exit 1
	fi
	addClass=0
	if [ "$1" == "-c" ];then
		addClass=1
	fi
	for name in $@;do
		if [ "$name" != "-c" ];then
			className="$(echo "$name" | sed 's/.*/\u&/')"
			if [ $addClass -eq 1 ];then
				name="Class$name"
			fi
			cpp="$name.cpp"
			hpp="$name.hpp"
			nameUpper=$(echo $name | tr a-z A-Z)
			checkFileExist $cpp
			checkFileExist $hpp
			setClass
			setHeader
		fi
	done
}

createClass $@