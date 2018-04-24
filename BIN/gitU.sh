#!/usr/bin/env bash
IFS=$'\n'
# assumes $GIT is a directory containing only git repos
if [[ "$1" =~ c ]]; then
	function git_command {
		git gc 2> /dev/null && echo "$b${dir##*/}$n done"
	}
else
	function git_command {
		git -c color.ui=always pull --recurse-submodules=on-demand 2> /dev/null \
			| sed -e "s/\(Already\|remote\)/$cr$b${dir##*/}$n/" \
			      -e "s/^Updating/$b${dir##*/}$n:/"
	}
fi
b=$(tput bold)
n=$(tput sgr0)
cr=$(tput cr)

# add pass store dir
command -v pass > /dev/null 2>&1 \
	&& [ -z "${PASSWORD_STORE_DIR:-}" ] \
	&& PASSWORD_STORE_DIR="$HOME/.password-store"

for dir in $GIT/* $PASSWORD_STORE_DIR; do
	cd "$dir"
	git_command &
done
wait 

