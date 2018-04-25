#!/usr/bin/env bash
IFS=$'\n'
# assumes $GIT is a directory containing only git repos
case $1 in
	c)
		function git_command {
			git -C $dir gc 2> /dev/null && echo "$b${dir##*/}$n done"
		} ;;
	p )
		function git_command {
			# will fail a lot for repos I don't have access to
			git -C $dir push 2> /dev/null && echo "$b${dir##*/}$n done"
		} ;;
	*)
		function git_command {
			git -C $dir -c color.ui=always pull --recurse-submodules=on-demand 2> /dev/null \
				| sed -e "s/\(Already\|remote\)/$cr$b${dir##*/}$n/" \
					  -e "s/^Updating/$b${dir##*/}$n:/"
		} ;;
esac
b=$(tput bold)
n=$(tput sgr0)
cr=$(tput cr)

# add pass store dir
command -v pass > /dev/null 2>&1 \
	&& [ -z "${PASSWORD_STORE_DIR:-}" ] \
	&& PASSWORD_STORE_DIR="$HOME/.password-store"

for dir in $GIT/* $PASSWORD_STORE_DIR; do
	git_command &
done
wait 

