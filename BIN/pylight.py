#!/data/data/com.termux/files/usr/bin/env python3

from optparse import OptionParser
import re
import sys

parser = OptionParser()
parser.usage = "%prog expr [expr2 [...]] [options]"
parser.add_option("-l","--line", action="store_true", dest="match_line", help="match the whole line")
parser.add_option("-o","--only", action="store_false", dest="print_unmatched", help="Print only lines which match", default=True)
# opts: opts array
# args: leftover mass-options
(opts, args) = parser.parse_args()

"""
match: list of regexes to match

compiles every argument
"""
matches = list()
color = [
            # bolded colors
            '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m',
            '\033[1m', # bolded default
            # unbolded colors
            '\033[0;31m', '\033[0;32m', '\033[0;33m', '\033[0;34m', '\033[0;35m', '\033[0;36m',
            # reverse colors
            '\033[7;31m', '\033[7;32m', '\033[7;33m', '\033[7;34m', '\033[7;35m', '\033[7;36m',
            '\033[7m' # reversed default
            # underline colors
            '\033[4;31m', '\033[4;32m', '\033[4;33m', '\033[4;34m', '\033[4;35m', '\033[4;36m',
            '\033[4m' # underlined default
        ]
num_colors = len(color)
reset_color = '\033[0m'
if opts.match_line:
    for arg in args:
        matches.append(re.compile(".*{0}.*".format(arg)))
else:
    for arg in args:
        matches.append(re.compile(arg))

for line in sys.stdin:
    matched = False
    for i,match in enumerate(matches):
        # search: match regex anywhere in line
        matches_on_line = match.finditer(line)
        rebuilt_line = ''
        last_match_end = 0
        if matches_on_line:
            for m in matches_on_line:
                # replace line with its colored split
                rebuilt_line += (line[last_match_end:m.start()]
                                 # if more matches than color, use the last available
                                 # color for all remaining matches
                                 + color[i if num_colors > i else num_colors - 1]
                                 + m.group()
                                 + reset_color)
                matched = True
                # if the full line is highlighted and printed, we can break on the first match
                last_match_end = m.end()
                if opts.match_line:
                    break
            line = rebuilt_line + line[last_match_end:]
    if matched or opts.print_unmatched:
        print(line, end = '')
