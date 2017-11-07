#!/usr/bin/env bash
shopt -s dotglob
if [[ -n $ANDROID_DATA ]]; then
	link_by() {
		echo Copying "$1 -> $2"
		cp $1 $2; chmod +x $2
	}
else
	link_by() {
		echo Creating link "$2 -> $1"
		ln -s $1 $2
	}
fi
cd BIN
for file in * 
do
	echo $file
	link_by $(pwd)/$file $HOME/.local/bin/${file%.*}
done
