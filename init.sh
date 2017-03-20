#!/usr/bin/env sh
cd BIN
for file in * 
do
	echo Symlinking $file
	ln -s $(pwd)/$file $HOME/.local/bin/$file
done
