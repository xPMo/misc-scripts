#!/usr/bin/env zsh
if [[ $- == *i* ]]; then
	(
		echo $fpath
		setopt NULL_GLOB
		function __test_comp {
			if [ ! -d "$1" ] && [ ! -f "$1.zwc" ] || [ "$1.zwc" -ot "$1" ]; then
				# echo "Compiling $1..."
				# -U: do not expand aliases
				zcompile -U $1
			fi
		}
		function __indir {
			cd $1
			# all files begining with z or .z and not ending with .zwc
			for f in .z*[^(\.zwc)] z*[^(\.zwc)]; do
				__test_comp $1
			done
		}
		for d in $fpath; do
			for f in $d/*[^(\.zwc)]; do 
				# ignore readme.mds
				if [[ ! $f =~ "\.md$" ]] ; then
					__test_comp $f
				fi
			done
		done
		__indir $HOME
		(( ${+ZDOTDIR} )) && __indir $ZDOTDIR
	)
else
	echo "This must be \`source\`d. It relies on your env \$fpath. (If you trust this, run with \`sudo su source\` to compile /usr/share/zsh/*)"
fi
