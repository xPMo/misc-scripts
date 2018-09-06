#!/usr/bin/env sh
set -e
IFS='
	'
[ ${DTACH_SOCKET:-} ] && exit 1
socket_dir="${PREFIX}/tmp"
socket_dir="$(mktemp --tmpdir=${socket_dir} --directory dtach.XXX)"
export DTACH_SOCKET="${socket_dir}/sock"
exec dtach -A $DTACH_SOCKET $SHELL
