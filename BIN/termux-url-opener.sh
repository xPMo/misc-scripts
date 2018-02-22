#!/data/data/com.termux/files/usr/bin/zsh
br="\033[1;31m%s\033[0m"
lock="$PREFIX/tmp/.url.queue.lock"
queue="$HOME/url.queue"

function get_f {
	echo -n "Specify variable name: "
	read y
	if (( ${+y} )); then
		eval $y=$(locate '*' | fzf)
		eval __temp="\$$y"
		echo "$y has been set to $__temp"
	else
		echo -n "No variable name given."
	fi
}

function get_d {
	cd $(find -L / -mindepth 1 \( -path '*/\\.*' -o -fstype 'sysfs' -o -fstype 'devfs' -o -fstype 'devtmpfs' \) -prune -o -type d -print | fzf)
}


if (( ${+1} )); then
	printf "$br%s\n" w "get"
	printf "$br%s\n" W "get, add arguments"
	printf "%s$br%s\n" "youtube-dl, e" x "tract audio"
	printf "$br%s\n" y "outube-dl"
	printf "$br%s\n" Y "outube-dl, add arguments"
	read y
	case $y in
	w)
		echo "cd $HOME/Downloads; wget --continue $1" >> $queue
	;;
	x)
		echo "cd $HOME/Music/youtube-dl; youtube-dl -x $1" >> $queue
	;;
	y)
		echo "cd $HOME/Videos; youtube-dl $1" >> $queue
	;;
	W)
		help="wget --help"
		cmd="wget --continue"
		;&
	Y)
		help="youtube-dl --help"
		cmd="youtube-dl"
		;&
	*)
		function print_opts {
			(( ${+help} )) && printf "%s$br%s\n" "get " h "elp"
			printf "%s$br%s\n" "print this " H "elp"
			printf "%s$br%s\n" "specify " p "ath"
			printf "%s$br%s\n" "make new " F "ile"
			printf "%s$br%s\n" "specify " d "irectory to run command in"
			printf "%s$br%s\n" "make new " D "irectory"
			print -n "    (currently "; print -rDn $PWD; print ")"
			printf "%s$br%s\n" "provide " a "rguments"
			echo -e "\nAvoid setting \$cmd, \$help, \$br, \$y, \$queue, \$lock, or \$__temp"
		}
		if [[ ! -n $cmd ]]; then
			echo "Specify command to run:"
			read cmd
			echo "What is the help command for $cmd?"
			read help
		fi
		print_opts
		while [[ $y != "a" ]]; do
			read y
			case $y in
			h)
				eval $help
				;;
			H)
				print_opts
				;;
			p)
				get_f
				;;
			F)
				echo -n "touch "; print -rDn $PWD; echo -n "/"
				read y
				touch $y
				;;
			d)
				get_d
				;;
			D)
				echo -n "mkdir "; print -rDn $PWD; echo -n "/"
				read y
				mkdir $y
				;;
			esac
		done
		unset y
		clear
		while
			eval $help
			[[ ! -n $y ]]
		do
			echo -n "In "; print -rD $PWD
			echo "Use \$1 as the URL"
			read y
		done
		args=$(echo $y | envsubst)
		echo "cd $PWD; $cmd $args" >> $queue
		;;
	esac
fi

if [ -f $lock ]; then
	echo "Lock exists. Another instance is running or did not exit cleanly"
	exit 0
fi

unset int
trap 'int=1' SIGINT
touch $lock
remain=$(mktemp "$PREFIX/tmp/.url.queue.XXXXXX")
while read cmd; do
	if [ $int ]; then
		echo $cmd >> $remain
	else
		eval $cmd || echo $cmd >> $remain
	fi
done < $queue
mv $remain $queue
rm $lock
