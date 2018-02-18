#!/data/data/com.termux/files/usr/bin/zsh
echo "extract audio? [y/n/o]"
read y
case $y in
	y)
		cd Music/youtube-dl
		youtube-dl -x $1 
	;;
	n)
		cd Videos
		youtube-dl $1
	;;
	*)
		echo "NOTE: the url provided to Termux is in \$1"
		echo "Okay, you're in $(pwd), something to do first? [y/n]"
		read y
		while [$y != 'n' ]; do
			read cmd
			$cmd
			echo "Okay, you're in $(pwd), something else to do first? [y/n]"
			read y
		done
		echo "Arguments for youtube-dl?"
		read cmd
		youtube-dl $cmd $1
	;;
esac


