#!/usr/bin/env bash
if echo $1 | egrep -q '^[0-9]+(.5)?$'; then
	newfont=$(xrdb -query | grep 'urxvt\*font:' | cut -f 2- | sed "s/size=[0-9.]*/:size=$1/")
else
	newfont=$(xrdb -query | grep 'urxvt\*font:' | cut -f 2-)
fi
echo -ne "\033]710;$newfont\033\\"
