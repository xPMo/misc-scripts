#!/usr/bin/env sh
set -e
IFS='
	'
[ ${DTACH_SOCKET:-} ] && {
	echo >&2 "unset DTACH_SOCKET or exit dtach"
	exit 1
}
dir=$PREFIX/tmp/dtach-$USER
mkdir -p $dir
export DTACH_SOCKET="${dir}/${1:-sock}"
dtach -A $DTACH_SOCKET $SHELL
