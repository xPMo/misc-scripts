#!/usr/bin/env bash
USAGE="Usage: $0 [ -f ] [ -c config ] COMPARE [ MATCH ]

Find the status of the two snapshots defined in COMPARE using
\`snapper status\`. By default, shows \`snapper diff\` of them
through \`less\`.

COMPARE: (N, M whole numbers:)
	N         	Diff snapshot N with snapshot 0 (current state)
	bN        	Diff the Nth most recent snapshot with snapshot 0
	pN        	Diff the Nth most recent pre-post pair
	N..M      	Diff the snapshots N and M

	-f        	call fzf on the diff list. Use MATCH as the initial query
	-c CONFIG 	use CONFIG with snapper instead of the default
"
snapper_cmd="snapper"

differ() {
	local files=()
	trap '{ rm "${files[@]}"; exit }' INT
	while read line; do
		file=$(mktemp)
		if [[ $line =~ $1 ]]; then
			$snapper_cmd diff "$s" $f \
			| sed -e "2 s/^/$bgrn/; 1 s/^/$bred/; s/^+/$grn+/; s/^-/$red-/; s/^@/$blu/" \
			> $file
			files+=($file)
		fi
	done
	if [ ! $files ]; then
		>&2 echo "No files changed"
		exit 0
	fi
	less -R "${files[@]}"
	rm "${files[@]}"
}

while getopts ":fc:" opt; do
	case "${opt}" in
	f)
		differ(){
			echo $s
			fzf --query="${1:-""}" --multi --ansi --preview \
				"snapper diff \"$s\" {+} \
				| sed -e \"2 s/^/$bgrn/; 1 s/^/$bred/; s/^+/$grn+/; s/^-/$red-/; s/^@/$blu/; s/^ /$res/\"" \
				--preview-window=up:60%
		}
		;;
	c) snapper_cmd="$snapper_cmd -c ${OPTARG}" ;;
	esac
done
shift $(( OPTIND - 1))

if [ "$#" -eq 0 ]; then
	echo "$USAGE"
	exit 1
elif [[ $1 =~ ^p[0-9]*$ ]]; then
	# compare n-th most recent pre-post pair
	line="${1:1}"
	s="$($snapper_cmd list --type pre-post | tail -n"${line:-1}" | head -n1 | cut -d\| -f -2 | xargs | sed 's/ | /../')"
elif [[ $1 =~ ^[0-9]+..[0-9]+$ ]]; then
	# raw pair
	s="$1"
elif [[ $1 =~ ^b[0-9]*$ ]]; then
	s="$($snapper_cmd list | tail -n$(( ${1:1} )) | head -n1 | cut -d\| -f2 | xargs)..0"
elif (( $1 > 0 )); then
	# snapshot value
	s="$(( $1 ))..0"
else
	echo "$USAGE"
	exit 1
fi

IFS=$'\n'
red=$'\033[31m'
grn=$'\033[32m'
blu=$'\033[34m'
bred=$'\033[31;1m'
bgrn=$'\033[32;1m'
res=$'\033[0m'
$snapper_cmd status "$s" | grep "^c....*" | cut -f2- -d ' ' | differ "$2"
