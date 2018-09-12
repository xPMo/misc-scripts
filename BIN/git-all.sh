#!/usr/bin/env bash
IFS=$'\n'
# assumes $GIT is a directory containing only git repos
case $1 in
	u|pu|pull)
		function git_command {
			git -C $1 -c color.ui=always pull --recurse-submodules=on-demand 2> /dev/null |
				sed -e "s/\(Already\|remote\)/$cr$b${1##*/}$n/" -e "s/^Updating/$b${1##*/}$n:/"
		} ;;
	* ) # parse as command
		cmd=$1
		function git_command {
			git -C $1 -c color.ui=always $cmd 2> /dev/null &&
				echo "$b${dir##*/}$n done" ||
				echo "$b${dir##*/}$n failed"
		} ;;
esac
b=$(tput bold)
n=$(tput sgr0)
cr=$(tput cr)

# add pass store dir
command -v pass > /dev/null 2>&1 &&
	[[ -z "${PASSWORD_STORE_DIR:-}" ]] &&
	PASSWORD_STORE_DIR="$HOME/.password-store"

echo "$GIT_REPO_PATH" | IFS=':' read -ra dirs
for dir in "${dirs[@]}" $PASSWORD_STORE_DIR; do
	git_command $dir &
done
wait 

