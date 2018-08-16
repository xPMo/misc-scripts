#!/usr/bin/env sh
set -euf
IFS='
	'

dir=$(git rev-parse --show-toplevel)

if grep --quiet --fixed-strings '[user]' $dir/.git/config; then
	echo >&2 "[user] config already exists"; exit 1
fi
cat $HOME/Sync/default/gitconfig/$1 >> $dir/.git/config
