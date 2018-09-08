#!/usr/bin/env sh
set -euf
IFS='
	'
pass show git.user/$1 |
while IFS=':' read key val; do
	val=$(echo $val| xargs)
	$echo git config user.$key $val
done
