#!/usr/bin/env sh
# shellcheck disable=2046
exec screenkey --font-size small $(xrdb -query | awk -f /dev/fd/3 3<< 'EOF' ) "$@"
/^\*background:/{
	print "--bg-color",$2
}
/^\*foreground:/{
	print "--font-color",$2
}
EOF
