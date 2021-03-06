#!/data/data/com.termux/files/usr/bin/bash
br="\033[1;31m%s\033[0m"
lock="${PREFIX:-/data/data/com.termux/files/usr}/tmp/.url.queue.lock"
queue="$HOME/url.queue"

# specify a variable name, and use fzf to set a useful value to it
# (like a filename for output)
get_f() {
	echo -n "Specify variable name: "
	read y
	if (( ${+y} )); then
		eval $y=$(locate '*' | fzf)
		eval _tmp="\$$y"
		echo "$y has been set to $_tmp"
	else
		echo -n "No variable name given."
	fi
}

# cd to a directory using fzf
get_d() {
	cd $(find -L / -mindepth 1 \( -path '*/\\.*' -o -fstype 'sysfs' -o -fstype 'devfs' -o -fstype 'devtmpfs' \) -prune -o -type d -print | fzf)
}

# print help for cutomizing script
print_opts() {
	(( ${+_h} )) && printf "%s$br%s\n" "get $_c " h "elp"
	printf "%s$br%s\n" "print this " H "elp"
	printf "%s$br%s\n" "specify " p "ath"
	printf "%s$br%s\n" "make new " F "ile"
	printf "%s$br%s\n" "specify " d "irectory to run command in"
	printf "%s$br%s\n" "make new " D "irectory"
	printf "%s$br%s\n" "provide " a "rguments"
	echo -e "\nAvoid setting _c, _h, br, y, queue, lock, _tmp"
	print -rD $PWD
}

if (( ${+1} )); then
	printf "$br%s\n" w "get"
	printf "$br%s\n" W "get, add arguments"
	printf "%s$br%s\n" "youtube-dl, e" x "tract audio"
	printf "$br%s\n" y "outube-dl"
	printf "%s$br%s\n" "youtube-dl, choose " f "ormat"
	printf "$br%s\n" Y "outube-dl, add arguments"
	read y
	case $y in

	# Default commands
	w)
		echo "cd $HOME/Downloads; wget --continue \"$1\"" >> $queue ;;
	x)
		echo "cd $HOME/Music/youtube-dl; youtube-dl -x \"$1\"" >> $queue ;;
	y)
		echo "cd $HOME/Videos/youtube-dl; youtube-dl \"$1\"" >> $queue ;;
	f|F)
		format="$(youtube-dl -F "$1" | sed -n '/^[0-9]/p' |
			fzf --multi --prompt='Format(s): ' | cut -d\  -f1)"
		format="${format%%'+'}"
		echo "cd $HOME/Videos/youtube-dl; youtube-dl \"$1\" -f $format" >> $queue
		;;

	# Fined-grained control
	W)
		_c="wget --continue"
		_h="wget --help"
		;& # requires bash >=4.0
	Y)
		_c="youtube-dl"
		_h="youtube-dl --help"
		;&
	*)
		if [[ ! -n $_c ]]; then
			echo "Specify command to run:"
			read _c
			echo "What is the help command for $_c?"
			read _h
		fi
		print_opts
		while [[ $y != "a" ]]; do
			read y
			case $y in
			h)
				eval $_h
				;;
			H)
				print_opts
				;;
			p)
				get_f
				;;
			F)
				echo -n "touch "
				read y
				touch $y
				;;
			d)
				get_d
				;;
			D)
				echo -n "mkdir -p"
				read y
				mkdir $y
				;;
			esac
		done
		unset y
		clear
		while
			eval $_h
			[[ ! -n $y ]]
		do
			echo -n "In "; print -rD $PWD
			echo "Use \$1 as the URL"
			read y
		done
		args=$(echo $y | envsubst)
		echo "cd $PWD; $_c $args" >> $queue
		;;
	esac
fi

if [ -f $lock ]; then
	echo "Lock exists. Another instance is running or did not exit cleanly"
	exit 0
fi

success=0
total=0
unset sig
trap 'sig=1' SIGINT
touch $lock
remain=$(mktemp "$PREFIX/tmp/.url.queue.XXXXXX")
while read line; do
	if [[ "${sig:-}" ]]; then
		# Don't run commands once signal recieved
		echo $line >> $remain
		(( total += 1 ))
	else
		eval $line && (( success += 1 )) || echo $line >> $remain
		(( total += 1 ))
	fi
done < $queue
mv $remain $queue
rm $lock
# Notify user of $queue status
#
if  (( success == total )); then
	termux-notification --id url --title "Termux URL Opener | Termux:API" \
		--content "All URLs processed successfully. ($total/$total)"
else
	termux-notification --id url --title "Termux URL Opener | Termux:API" \
		--content "Results: $success/$total" \
		--button1 "Try again" --button1-action "$0"
fi
