#!/usr/bin/env bash
# Update it all (apt/pkg/pacaur, $GIT/*)
b=$(tput bold)
n=$(tput sgr0)
cr=$(tput cr)
l=()
for dir in $GIT/*; do
	cd "$dir"
	git pull 2> /dev/null | sed "s/\(Already\|remote\)/$cr$b${dir##*/}$n/" &
done
wait 

