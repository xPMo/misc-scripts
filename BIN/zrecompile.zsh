if [[ $- == *i* ]]; then
	(
	echo $fpath
	setopt NULL_GLOB
	function __test_comp {
		if [ ! -d "$1" ] && [ ! -f "$1.zwc" ] || [ "$1.zwc" -ot "$1" ]; then
			# echo "Compiling $1..."
			zcompile $1
		fi
	}
	function __indir {
		cd $1
		# all files begining with z or .z and not ending with .zwc
		for f in .z*[^(\.zwc)] z*[^(\.zwc)]; do
			test_comp $1
		done
	}
	for d in $fpath; do
		for f in $d/*[^(\.zwc)]; do 
			# ignore readme.mds
			if [[ ! $f =~ "\.md$" ]] ; then
				test_comp $f
			fi
		done
	done
	__indir $HOME
	(( ${+ZDOTDIR} )) && __indir $ZDOTDIR
	)
else
	echo This must be sourced. It relies on your fpath.
fi
