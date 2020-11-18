
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
	done < $className.hpp
	if [ $lineAdd -eq 0 ];then
		echo "Error: no public member found in $className.hpp"
		exit 1
	fi
	if [ -z "$buffClass" ];then
		echo "No attrubut in $className.hpp"
		exit 1
	fi
	((lineAdd++))
	sed -i "${lineAdd}"'i\'"$buffHeader" $className.hpp
	printf "$buffClass" >> $className.cpp

}

function	checkExistClassHeader {
	headerFilename=$(echo $file | sed 's/.cpp/.hpp/g')
	className=$(echo $file | sed 's/.cpp//g')
	if [ ! -f $file ];then
		echo "File $file not found"
	elif [ ! -f $headerFilename ];then
		echo "File $headerFilename not found"
	else
		makeSetGet
	fi
}

function	generateSetGet {
	if [ -n $1 ];then
		for file in $@; do
			file="$file.cpp"
			checkExistClassHeader
		done
	else
		for file in *.cpp; do
			checkExistClassHeader
		done
	fi
}

generateSetGet $@