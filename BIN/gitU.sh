#!/usr/bin/env bash
IFS=$'\n'
# assumes $GIT is a directory containing only git repos
if [[ "$1" =~ c ]]; then
	function git_command {
		git gc 2> /dev/null && echo "$b${dir##*/}$n done"
	}
else
	function git_command {
		git pull --recurse-submodules=on-demand 2> /dev/null \
			| sed "s/\(Already\|remote\)/$cr$b${dir##*/}$n/"
	}
fi
b=$(tput bold)
n=$(tput sgr0)
cr=$(tput cr)
for dir in $GIT/*; do
	cd "$dir"
	git_command &
done
wait 

