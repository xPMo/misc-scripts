#!/usr/bin/env bash
shopt -s dotglob
if [[ -n $ANDROID_DATA ]]; then
	link_by() {
		diff "$1" "$2" -q 2>/dev/null || (
			echo "Copying $1 -> $2"
			cp $1 $2
			chmod +x $2
		)
	}
	cd termux-BIN
	for file in *; do
		link_by $(pwd)/$file $HOME/.local/bin/${file%.*}
	done
	cd ..
else
	link_by() {
		[ -L "$2" ] && return
		if [ -f "$2" ]; then
			echo "$2 exists and is not a symlink. Linking to $2.new"
			ln -s "$1" "$2.new"
		else
			ln -s "$1" "$2"
		fi
	}
fi
cd BIN
for file in *; do
	link_by $(pwd)/$file $HOME/.local/bin/${file%.*}
done
cd ..
