#!/usr/bin/env sh
set -eufx
IFS='
	'

insert_all() {
	while
		read label
		read secret
	do
		insert $secret $label
		echo "$secret $label"
	done
}

insert() {
	prefix=${PASSWORD_STORE_DIR:-$HOME/.password-store}

	f=$(
		find $prefix -iname '*.gpg' |
			sed -e "s:^${prefix}/::" -e "s/....$//" |
			rofi -p "$2" -dmenu -i
	)
	echo "$1" | pass otp append --issuer $(basename $(dirname $f)) $f --secret
}

gpg --decrypt "$1" | jq --raw-output '.[] | .label, .secret' | insert_all
