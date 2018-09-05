#!/usr/bin/env bash

function urxvt-set {
	local val
	if [ -z $pattern ]; then usage; exit 1; fi
	val="$(xrdb -query | grep -i -E $pattern | cut -f 2- | sed -e ${replace:-' '} )"
	echo -ne "\033]$code;$val\033\\"
}
function usage {
cat >&2 << EOF
$(basename $0) [ option [ value ]]

Uses escape codes to set urxvt settings. Settings must exist
in \`xrdb -query\`.  If no value is provided, setting is reset
to the xrdb-provided default.

	-o --opacity     sets the opacity of the terminal background
	-b --background  sets the terminal background as [%%]#XXXXXX
	-f --font        sets the size of the terminal font
	-h --help        print this help
EOF
}

case $1 in

	-h ) ;&
	--help )
		usage
		exit 0
		;;
	-b ) ;&
	--background )
		shift
		code=49
		pattern='urxvt.background:'
		if [[ $1 =~ ^\[1?[0-9]?[0-9]\]#[0-9a-fA-F]{6,6}$ ]]; then
			replace="s/.*/$1/"
			shift
		fi
		;;

	-o ) ;&
	--opacity )
		shift
		code=49
		pattern='urxvt.background:'
		if [[ $1 =~ ^1?[0-9]?[0-9]$ ]]; then
			replace="s/\[[0-9]*\]/[$1]/"
			shift
		fi
		;;

	-f ) ;&
	--font )
		shift
		code=710
		pattern='urxvt.font:'
		if [[ $1 =~ ^[0-9]+(.5)?$ ]]; then
			replace="s/size=[0-9.]*/:size=$1/"
			shift
		fi
		;;

esac
urxvt-set
