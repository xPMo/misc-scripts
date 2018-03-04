#!/usr/bin/env bash
USAGE="Usage: $0 <index1>..<index2> [ <match> ]

Prints out diffs of all files differing between snapshots
<index1> and <index2> and whose paths are matched by <match>."

if [ "$#" -eq 0 ]; then
	echo $USAGE
	exit 1
elif [[ $1 =~ ^[a-z][0-9]*$ ]]; then
	# compare n-th most recent pre-post pair
	line=${1:1}
	s="$(snapper list --type pre-post | tail -n"${line:-1}" | head -n1 | cut -d\| -f -2 | xargs | sed 's/ | /../')"
elif [[ $1 =~ ^[0-9]+..[0-9]+$ ]]; then
	# raw pair
	s="$1"
elif (( $1 < 0 )); then
	# -n snapshots ago
	s="$(snapper list | tail -n$(( -$1 )) | head -n1 | cut -d\| -f2 | xargs)..0"
elif (( $1 > 0 )); then
	# snapshot value
	s="$(( $1 ))..0"
else
	echo $USAGE
	exit 1
fi

IFS=$'\n'
red=$'\033[31m'
grn=$'\033[32m'
blu=$'\033[34m'
bred=$'\033[31;1m'
bgrn=$'\033[32;1m'
files=()
trap '{ rm "${files[@]}"; exit }' INT
for f in $(snapper status "$s" | grep "^c....*$2" | cut -f2- -d ' '); do
	file=$(mktemp)
	snapper diff "$s" $f \
		| sed -e "2 s/^/$bgrn/; 1 s/^/$bred/; s/^+/$grn+/; s/^-/$red-/; s/^@/$blu/" \
		> $file
	files+=($file)
done
if [ ! $files ]; then
	>&2 echo "No files changed"
	exit 0
fi
less -R "${files[@]}"
rm "${files[@]}"
