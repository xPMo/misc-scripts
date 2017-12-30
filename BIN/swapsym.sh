#!/usr/bin/env bash
# Provided a symlink, will replace the symlink with the source file/dir
# and place a symlink in the original location

[! -L $1 ] && echo "$1 is not a symlink" && return 1

$dirtarget=$(realpath $(dirname $1) --relative-to=$(readlink $1))
$file="$(readlink $1)"
rm $1
mv "$file" $dirtarget/$1
ln -s $(realpath $dirtarget/$1)
