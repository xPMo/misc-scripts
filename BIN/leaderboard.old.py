#!/usr/bin/env python3

# This is the old version, using HTMLParser
# The xml version is much better, use it.

from optparse import OptionParser
from html.parser import HTMLParser
import re
import urllib.request
class TrackPageParser(HTMLParser):
    """
    HTML Parser

    For some reason "score"'s data has a bunch of \t's in it.
    Not sure why.
    """
    # Looking for attr = lbentry
    # relativeRank - playerName - score
    def __init__(self):
        HTMLParser.__init__(self)
        self.print_data = False
        self.print_newline = False
    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.print_data = True
            self.print_newline = True
            return
        for attr in attrs:
            if attr == ("class","rR"):
                self.print_data = True
                return
            if attr == ("class","playerName"):
                self.print_data = True
                return
            if attr == ("class","score"):
                self.print_data = True
                self.print_newline = True
                return
    def handle_endtag(self, tag):
        self.print_data = False
        self.print_newline = False
    def handle_data(self, data):
        if self.print_data:
            print("{0}{1}".format(re.sub(r"\\t\\t\\t\\t", "", data),
                                  "\n" if self.print_newline else " "),
                  end='', flush=True)
# Track IDs
tracks = {
    "sprint": {
        "broken symmetry": "1558337",
        "lost society": "1558158",
        "negative space": "1558398",
        "departure": "1558402",
        "friction": "1558436",
        "aftermath": "1558394",
        "the thing about machines": "1558441",
        "amusement": "1558304",
        "corruption": "1558416",
        "the observer effect": "1558453",
        "dissolution": "1558428",
        "falling through": "1558435",
        "monolith": "1558429",
        "uncanny valley": "1558467"
    },
    "challenge": {
        "dodge": "1558764",
        "thunder struck": "1558769",
        "grinder": "1558800",
        "descent": "1558836",
        "detached": "1558817",
        "elevation": "1558823"
    },
    "stunt": {
        "credits": "1588771",
        "refraction": "1589164",
        "space skate": "1561263",
        "spooky town": "1573802",
        "stunt playground": "1561573",
        "tagtastic": "1572280"
    }
}
# """
# Option parsing
# """
parser = OptionParser()
parser.usage = "%prog level [level2 [...]] [options] (level is a regular expression)"
parser.add_option("-m","--mode",action="store", default=".", dest="mode", help="Mode to lookup. Searches all by default")
# parser.add_option("-g","--game-id", action="store", default='233610', dest="gameid", help="Game id to be used. Defaults to Distance. (You can try if you want.)")
(opts, args) = parser.parse_args()

def lookup(gameid, levelid):
    url = 'http://steamcommunity.com/stats/' + gameid + '/leaderboards/' + levelid
    # Make the request object
    req = urllib.request.urlopen(url)
    board_parser = TrackPageParser()
    board_parser.feed(str(req.read()))
# """
# main
# """
for mode, track_list in tracks.items():
    if re.search(opts.mode.lower(), mode):
        for name, val in track_list.items():
            for arg in args:
                if re.search(arg.lower(), name):
                    lookup('233610',val)
                    break