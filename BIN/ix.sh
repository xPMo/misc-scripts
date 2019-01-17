#!/usr/bin/env sh

# Examples:
#     ix hello.txt              # paste file (name/ext will be set).
#     echo Hello world. | ix    # read from STDIN (won't set name/ext).
#     ix -n 1 self_destruct.txt # paste will be deleted after one read.
#     ix -i ID hello.txt        # replace ID, if you have permission.
#     ix -d ID
[ -f "$HOME/.netrc" ] && opts='-n'
while getopts ":hd:i:n:" x; do
	case $x in
		h) 
			cat >&2 << EOF
$(basename $0) [-d ID] [-i ID] [-n N] [curl opts]

	-d ID   delete the given ID
	-i ID   replace the given ID
	-n N    delete the paste after N reads
	-h      show this help

Curl can work with a filename or stdin. If a filename is
provided, ix.io will set the name on the paste.
EOF
			exit 0;;
		d)
			curl $opts -X DELETE ix.io/$OPTARG
			exit $?;;
		i) opts="$opts -X PUT"; id="$OPTARG";;
		n) opts="$opts -F read:1=$OPTARG";;
	esac
done
shift $((OPTIND - 1))
if [ -t 0 ]; then
	filename="$1"
	shift
	[ "$filename" ] && {
		curl $opts -F f:1=@"$filename" $@ ix.io/$id
		exit $?
	}
	echo "^C to cancel, ^D to send."
fi
curl $opts -F f:1='<-' "$@" ix.io/$id
