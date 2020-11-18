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

function	ft_strchr {
	if [ -z "$2" ];then
		return 0
	fi
	case "$2" in
		*$1*)
		return 1
		;;
	esac
	return 0
}

function	prepareBuff {
	IFS=' 	' read -ra strarr <<< "$1"
	type=${strarr[0]}
	name=${strarr[1]}
	type="$type "
	name="${name::-1}"
	if [[ "$name" = \** ]];then
		type="$type*"
		name="${name:1}"
	fi
	u_name="$(echo "$name" | sed 's/.*/\u&/')";
	getter="get$u_name()"
	setter="set$u_name($type$name)"
	buffHeader="$buffHeader\n\t$type$getter;\n\tvoid $setter;"
	buffClass="$buffClass\n$type	$className::$getter\n{\n\treturn this->$name;\n}\n"
	buffClass="$buffClass\nvoid	$className::$setter\n{\n\tthis->$name = $name;\n}\n"
}

function 	makeSetGet {
	buffClass=""
	buffHeader=""
	private=1
	i=0
	lineAdd=0
	className="Chevalier"
	beginClass=0
	while read line;do
		((i++))
		ft_strchr "};" $line
		stopLook=$?
		if [ "$stopLook" -eq 1 ];then
			break
		elif [ $beginClass -eq 0 ];then
			ft_strchr "class" $line
			ret=$?
			if [ "$ret" == 1 ];then
				beginClass=1
			fi
		elif [ $beginClass -eq 1 ];then
			beginClass=2
		elif [ $private -eq 1 ];then
			ft_strchr public $line
			ret=$?
			ft_strchr "(" $line
			fnc=$?
			if [ "$ret" == 1 ];then
				private=0
				if [ $lineAdd -eq 0 ];then
					lineAdd=$i
				fi
			elif [ -n "$line" -a "$fnc" == 0 ];then
				prepareBuff "$line"
			fi
		elif [ $private -eq 0 ]; then
			ft_strchr private $line
			ret=$?
			if [ "$ret" == 1 ];then
				private=1
			fi
			ft_strchr $className $line
			str_chr=$?
			if [ "$str_chr" == 1 ];then
				lineAdd=$i
			fi
		fi
	done < Chevalier.hpp
	# printf "$lineAdd\n"
	if [ $lineAdd -eq 0 ];then
		echo "Error: not public segment found"
		exit 1
	fi
	if [ -z "$buffClass" ];then
		echo "No attrubut found"
	fi
	((lineAdd++))
	# printf "$buffClass\n$buffHeader\n"
	sed -i "${lineAdd}"'i\'"$buffHeader" Chevalier.hpp
	printf "$buffClass" >> Chevalier.cpp

}

makeSetGet
# createClass $@