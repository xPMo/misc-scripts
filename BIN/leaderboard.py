#!/usr/bin/env python3

from optparse import OptionParser
import xml.etree.ElementTree as ET
import re
import urllib.request
from threading import Thread
import unicodedata

# Track IDs for Distance
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
def get_key(path):
    """Gets your Steam web API key from the path provided."""
    return open(path, 'r').read

def lookup_board(key, gameid, levelid, count, parseTime=True):
    """Look up a track on the steam leaderboard

    This function handles printing its data as well

    Takes a gameid, leaderboardid, and a count and prints the top `count` entries
    in that leaderboard (calls lookup_steamid to get the profile name)
    """
    url = 'http://steamcommunity.com/stats/' + gameid + '/leaderboards/' + levelid + '/?xml=1&start=1&end=' + str(count)
    # Make the request object
    req = urllib.request.urlopen(url)
    xml_tree = ET.parse(req)
    root = xml_tree.getroot()
    ranks = []
    scores = []
    steamids = []

    for entry in root.find('entries').findall('entry'):
        # get relavent data out of 'entry'
        score = entry.find('score').text
        if parseTime:
            minutes, milliseconds = divmod(int(score), 60000)
            seconds = float(milliseconds) / 1000
            score = "%i:%06.3f" % (minutes, seconds)
        ranks.append(entry.find('rank').text)
        steamids.append(entry.find('steamid').text)
        scores.append(score)

    profiles = lookupsteamids(key, steamids)
        

def lookup_steamids(key, steamids, table):
    """Looks up a list of 64-bit steamids, makes an array of profile names

    Takes steamid (a numerical identifier)
    looks up and fetches the associated profile name
    """
    profiles = []
    url = 'http://steamcommunity.com/profiles/?key=' + key + '&steamids=' + ','.join(steamids) + '&xml=1'
    try:
        req = urllib.request.urlopen(url)
        xml_tree = ET.parse(req)
        root = xml_tree.getroot()
        for child in root:
            profiles.append(child.personastate.text)
    except urllib.error.HTTPError:
        pass
    return profiles

def nonspacing_count(s):
    """Counts the number of 'Nonspacing_Mark' characters in a string 's'"""
    count = 0
    for c in s:
        if unicodedata.category(c) == 'Mn':
            count += 1
    return count

# ==================
# MAIN program logic is here
# ==================

# Option parsing
parser = OptionParser()
parser.usage = "%prog level [level2 [...]] [options] (level is a regular expression)"
parser.add_option("-m", "--mode", action="store", default=".", dest="mode", help="Mode to lookup. Searches all by default")
# parser.add_option("-g","--game-id", action="store", default='233610', dest="gameid", help="Game id to be used. Defaults to Distance. (You can try if you want.)")
parser.add_option("-n", "--number", action="store", default=15, dest="count", help="Number of places to print. Views top 15 by default")
parser.add_option("-s", "--simple", action="store_false", default=True, dest="pretty", help="Disable pretty box drawings")
parser.add_option("-k", "--key-path", action="store", default="~/.local/steamapikey", dest="key_path" help="Path to Steam API key. ~/.local/steamapikey by default")
(opts, args) = parser.parse_args()

# Main loop
for mode, track_list in tracks.items():
    # limit mode to the mode requested
    if re.search(opts.mode.lower(), mode):
        for name, val in track_list.items():
            for arg in args:
                # limit tracks to tracks requested
                if re.search(arg.lower(), name):
                    timed = True
                    if mode == 'stunt':
                        timed = False
                    print("\n{:^50}".format( name.title() + ": " + mode.title()))
                    if(not opts.pretty):
                        print('{:^6} {:<33} {:^9}'.format('Rank', 'Player', 'Score' if timed else 'Score'))
                        lookup_board(get_key(opts.key_path), '233610', val, int(opts.count), parseTime=timed)
                        # Flush print buffer after each board
                        print('', flush=True, end='')
                    else:
                        print('┌──────┬──────────────────────────────────┬──────────┐')
                        print('│{:^6}│ {:<33}│{:^9} │'.format('Rank', 'Player', 'Score' if timed else 'Score'))
                        print('├──────┼──────────────────────────────────┼──────────┤')
                        lookup_board(get_key(opts.key_path), '233610', val, int(opts.count), parseTime=timed)
                        # Flush print buffer after each board
                        print('└──────┴──────────────────────────────────┴──────────┘', flush=True)
                    break
