#!/usr/bin/env bash
USAGE="Usage: $0 <index1>..<index2> [ <query> ]

fzf on all files differing between snapshots <index1> and <index2>.
Begin with <query>

If only a positive number is passed, diff <index> with 0.
If only a negative number is passed, diff <nth-most-recent> with 0.
If [a-z]\"<n>\" is passed, diff the nth-most recent pre-post pair."
if [ "$#" -eq 0 ]; then
	echo $USAGE
	exit 1
elif [[ $1 =~ ^[a-z][0-9]*$ ]]; then
	# compare n-th most recent pre-post pair
	s="$(snapper list --type pre-post | tail -n"${${1:1}:-1}" | head -n1 | cut -d\| -f -2 | xargs | sed 's/ | /../')"
elif [[ $1 =~ ^[0-9]+..[0-9]+$ ]]; then
	# raw pair
	s="$1"
elif (( $1 < 0 )); then
	# -n snapshots ago
	s="$(snapper list | tail -n$(( -$1 )) | head -n1 | cut -d\| -f2 | xargs)..0"
elif (( $1 > 0 )); then
	# snapshot value
	s="$( $1 | xargs)..0"
else
	echo $USAGE
	exit 1
fi

IFS=$'\n'
red=$(echo -e "\033[31m")
grn=$(echo -e "\033[32m")
blu=$(echo -e "\033[34m")
bred=$(echo -e "\033[31;1m")
bgrn=$(echo -e "\033[32;1m")
res=$(echo -e "\033[0m")
snapper status "$s" | grep "^c....*" | cut -f2- -d ' ' | \
	fzf $FZF_DEFAULT_OPTS --query="${2:-""}" --multi --ansi --preview \
		"snapper diff $s {+} \
		| sed -e \"2 s/^/$bgrn/; 1 s/^/$bred/; s/^+/$grn+/; s/^-/$red-/; s/^@/$blu/; s/^ /$res/\""
