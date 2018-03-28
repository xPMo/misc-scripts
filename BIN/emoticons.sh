#!/usr/bin/env sh

selection="$(
printf '%12s\t%s\n' \
"disapproval" "ಠ_ಠ" \
"lenny" "( ͡° ͜ʖ ͡°)" \
"music" "ヾ(⌐■_■)ノ♪" \
"pilfelbat" "┳━┳ ︵ /(.□. )\\" \
"pointatu" "(☞ﾟヮﾟ)☞" \
"shrug" "¯\\_(ツ)_/¯" \
"stroll" "(งツ)ว" \
"tableflip" "(╯°□°）╯︵ ┻━┻" \
"takemyenergy" "༼ つ ◕_◕ ༽つ" \
"y u no" "ლ(ಠ益ಠლ)" \
"zoidberg" "(/) (°,,°) (/)" \
| fzf -n1
)"

if command -v xclip > /dev/null; then
	echo "$selection" | cut -f2 | xclip -selection clipboard
elif command -v xsel > /dev/null; then
	echo "$selection" | cut -f2 | xsel -b
else
	echo "$selection" | cut -f2
fi
