#!/usr/bin/env bash
function usage {
	echo "$0 [ option [ value ]]
Uses escape codes to set urxvt settings. Settings must exist
in \`xrdb -query\`.  If no value is provided, setting is set
to xresources default.

	-o --opacity	sets the opacity of the terminal background
	-f --font   	sets the size of the terminal font
	-h --help   	print this help
	"
	exit 1
}
function urxvt-set {
	local val
	[ -z $name ] && exit 1
	val="$(xrdb -query | grep $name | cut -f 2- | sed -e ${replace:-' '} )"
	echo -ne "\033]$code;$val\033\\"
}
while true; do
	unset replace
	case $1 in
		--help ) ;&
		-h ) usage ;;
		--opacity ) ;&
		-o )
			shift
			code=49
			name='urxvt\*background:'
			if [[ $1 =~ ^1?[0-9]?[0-9]$ ]]; then
				replace="s/\[[0-9]*\]/[$1]/"
				shift
			fi
			;;
		--font ) ;&
		-f )
			shift
			code=710
			name='urxvt\*font:'
			if [[ $1 =~ ^[0-9]+(.5)?$ ]]; then
				replace="s/size=[0-9.]*/:size=$1/"
				shift
			fi
			;;
	esac
	urxvt-set
	unset name
done
