#!/usr/bin/env bash
IFS=$'\n'
# assumes $GIT is a directory containing only git repos
b=$(tput bold)
n=$(tput sgr0)
cr=$(tput cr)
for dir in $GIT/*; do
	cd "$dir"
	git pull 2> /dev/null | sed "s/\(Already\|remote\)/$cr$b${dir##*/}$n/" &
done
wait 

