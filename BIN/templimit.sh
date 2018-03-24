#!/usr/bin/env bash
IFS=$'\n'
TEMPLIMIT_MAX=${TEMPLIMIT_MAX:-100}
TEMPLIMIT_MIN=${TEMPLIMIT_MIN:-75}

function list_offspring {
	tp=$(ps -o pid= --ppid $1)
	for i in $tp; do
		if [ -z $i ]; then
			exit
		else
			echo $i
			list_offspring $i
		fi;
	done
}

function limit_pid {
	while state=$( ps -p "$1" -o state= ); do
		temp=$(( $(sensors -u \*-isa-\* | sed -n '/input/{s/.*input: \(.*\)\..*/\1/p; q}' ) ))
		case $state in
		[DRS] ) # running
			if (( temp > TEMPLIMIT_MAX )); then
				echo "Temperature at $temp, sending SIGSTOP to $1" >&2
				kill -SIGSTOP $1 $(list_offspring $1)
			fi
			;;
		[T] ) # stopped
			if (( temp < TEMPLIMIT_MIN )); then
				echo "Temperature at $temp, sending SIGCONT to $1" >&2
				kill -SIGCONT $1 $(list_offspring $1)
			fi
			;;
		* ) # idk
			;;
		esac
		sleep 2
	done
}

if ps -p "$1" >/dev/null; then
	limit_pid $1
else
	echo -e "Could not find process $1" >&2
	exit 1
fi
