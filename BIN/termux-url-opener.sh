#!/data/data/com.termux/files/usr/bin/zsh
br="\033[1;31m%s\033[0m"
lock="$PREFIX/tmp/.url.queue.lock"
queue="$HOME/url.queue"

printf "$br%s\n" w "get"
printf "%s$br%s\n" "youtube-dl w/e" x "tract"
printf "$br%s\n" y "outube-dl"
read y
case $y in
w)
	echo "cd $HOME/Downloads; wget --continue \'$1\'" >> $queue
;;
x)
	echo "cd $HOME/Videos; youtube-dl \'$1\'" >> $queue
;;
y)
	echo "cd $HOME/Music/youtube-dl; youtube-dl -x \'$1\'" >> $queue
;;
*)
	echo "NOTE: the url provided is \$1 ($1)"
	echo "Okay, you're in $(pwd), something to do first? [y/n]"
	read y
	while [$y != 'n' ]; do
		read cmd
		$cmd
		echo "Okay, you're in $(pwd), something else to do first? [y/n]"
		read y
	done
	echo "Command to run? (please provide the url w/'\$1'"
	read cmd
	# ${!var}: expand variable
	echo ${!cmd} >> $queue
;;
esac
if [ -f $lock ]; then
	echo "Lock exists. Another instance is running or did not exit cleanly"
	exit 0
fi

# cleanup sets __exit, which stops all remaining $cmd from executing
function cleanup {
	echo "Will cleanup and exit after $cmd"
	__exit=1
	return 0
}

trap cleanup SIGINT
touch $lock
remain=$(mktemp "$PREFIX/tmp/.url.queue.XXXXXX")
while read cmd; do
	if [ $__exit ]; then
		echo $cmd >> $remain
	else
		$cmd || echo $cmd >> $remain
	fi
done < $queue
mv $remain $queue
rm $lock
