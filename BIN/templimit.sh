#!/usr/bin/env bash
IFS=$'\n'
set -e

TEMPLIMIT_MAX=${TEMPLIMIT_MAX:-100}
TEMPLIMIT_MIN=${TEMPLIMIT_MIN:-75}

interval=2
verbose=1
chip='*-isa-*'

function usage {
cat >&2 << EOF
Usage: $(basename $0) [ -p PID ] | [ -x [ CMD [ ARGS ... ] ] | PID | CMD [ ARGS ... ]

Uses \`sensors\` to get temperature, and sends SIGSTOP and SIGCONT signals to
processes when the temperature crosses certain thresholds.

Options and arguments:
	-h           print this help
	-vh          print this help with help about verbosity levels
	-p PID       limit the process with pid PID and all its children
	-x CMD ARGS  run the given command in the background, and limit
	             it and all its children
	-X CMD ARGS  enable job control and run the command in the foreground,
	             and limit it and all its children
	-t TIME      set delay between temperature checks to TIME seconds
	-v           increase verbosity
	-q           decrease verbosity
	-c REGEX     Use REGEX to choose what chip to use. Defaults to *-isa-*

If none of \`-p\`, \`-x\`, or \`-X\` are provided, both PID and CMD methods will be tried

Environment variables:
	TEMPLIMIT_MAX:  if the temperature is above this value, send SIGSTOP
	                default is 100
	TEMPLIMIT_MIN:  if the temperature is below this value, send SIGCONT
	                default is 75

EOF
(( verbose > 1 )) && cat >&2 <<- EOF
Verbosity levels: [0-15], Default level is 1

	0:    Only fatal messages printed
	1-5:  Increasing information
	6:    Include debug level at head of line
	7:    Enable xtrace (\`set -x\`), disables levels 1-6
	8-15: Re-enables levels 1-6

EOF
}

function debug {
	unset head
	(( verbose < $1 )) && return
	(( verbose > 5 )) && head="\e[38;1mDEBUG[${1}]: " >&2
	case $1 in
		0 ) code='\e[38;1m'   ;; # bold
		1 ) code='\e[38;0m'   ;; # normal
		2 ) code='\e[38;5;6m' ;; # cyan
		3 ) code='\e[38;5;7m' ;; # faint
		* ) code='\e[38;5;8m' ;; # fainter
	esac
	echo -e "${code}${head}${2}\e[0m" >&2
}

function list_offspring {
	tp=$(ps -o pid:1= --ppid $1)
	debug 5 "Getting offspring: $tp"
	for i in $tp; do
		if [ -z $i ]; then
			exit
		else
			echo $i
			list_offspring $i
		fi;
	done
}

function pidtree {
	declare -A childs
	while read P PP;do
		CHILDS[$PP]+=" $P"
	done < <(ps -e -o pid= -o ppid=)

	walk() {
		echo $1
		for i in ${childs[$1]}; { walk $i; }
		}

	for i in "$@";do
		walk $i
	done
}


function limit_pid {
	debug 2 "Limiting process with pid $1"
	while state=$( ps -p "$1" -o state= ); do
		temp=$(( $(sensors -u $chip | sed -n '/input/{s/.*input: \(.*\)\..*/\1/p; q}' ) ))
		debug 3 "Temperature:   $temp"
		debug 4 "Process state: $state"
		case $state in
		[DRS] ) # running
			if (( temp > TEMPLIMIT_MAX )); then
				debug 2 "Temperature at $temp, sending SIGSTOP to $1"
				kill -SIGSTOP $1 $(list_offspring $1)
			fi
			;;
		[T] ) # stopped
			if (( temp < TEMPLIMIT_MIN )); then
				debug 2 "Temperature at $temp, sending SIGCONT to $1"
				kill -SIGCONT $1 $(list_offspring $1)
			fi
			;;
		* ) # idk
			;;
		esac
		sleep $interval
	done
	debug 2 "Process $1 has exited."
}

function try_execute {

	command -v "$1" > /dev/null 2>&1 || {
		debug 1 "Could not find command $1"
		return 1
	}

	(( ${exec_fg:-0} == 1 )) && {
		# enable job control
		set -m
		eval "$@" > /dev/null &
		pid="$!"
		limit_pid $pid &
		debug 1 "Foregrounding $@"
		fg %1
	} || {
		eval "$@" &
		pid="$!"
		limit_pid $pid
	}

}

function try_limit_pid {
	ps -p "$1" > /dev/null 2>&1 || {
		debug 1 "Could not find process with pid $1"
		return 1
	}
	limit_pid $1
}

while getopts ":t:c:hpvqxX" opt; do
	case $opt in
		h) usage; exit 0 ;;
		t) (( OPTARG > 0 )) && interval=${OPTARG} || { usage; exit 1; };;
		c) sensors $OPTARG && chip="$OPTARG" ;;
		p) use_pid=1 ;;
		x) exec_fg=0; use_pid=0 ;;
		X) exec_fg=1; use_pid=0 ;;
		q) (( verbose-- )) ;;
		v) (( verbose++ )) ;;
		*) usage; exit 1 ;;
	esac
done

if (( verbose > 6 )); then
	set -x
	(( verbose = verbose - 7 ))
fi

shift $(( OPTIND - 1 ))

(( $# )) || { usage; exit 1; }

case $use_pid in
	1) try_limit_pid "$1" ;;
	0) try_execute "$@" ;;
	*) try_limit_pid "$1" || try_execute "$@" ;;
esac
