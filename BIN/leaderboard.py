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

def lookup_board(gameid, levelid, count, parseTime=True):
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
    # each row is a dict(rank, score, uname)
    table = []
    # list of threads, blocks respective row until it is .join()'d
    threads = []

    for entry in root.find('entries').findall('entry'):
        # get relavent data out of 'entry'
        rank = entry.find('rank').text
        score = entry.find('score').text
        steamid = entry.find('steamid').text
        if parseTime:
            minutes, milliseconds = divmod(int(score), 60000)
            seconds = float(milliseconds) / 1000
            score = "%i:%06.3f" % (minutes, seconds)
        table_row = {'rank' : rank, 'score' : score}
        table.append(table_row)
        # 'table_row' is passed by reference, so lookup_steamid can edit that row of 'table'
        # without any kind of indexing shenanigans
        new_thread = Thread(target = lookup_steamid, args = (steamid, table_row))
        new_thread.start()
        threads.append(new_thread)

    # Wait on threads
    for thread, row in zip(threads, table):
        thread.join()
        # fix width problems for unicode nonspacing marks
        uname_width = 33 + nonspacing_count(row['uname'])
        if(opts.pretty):
            print("│{:>5} │ {:<{width}}│{:>9} │".format('#'+row['rank'], row['uname'], row['score'], width=uname_width))
        else:
            print("{:>5}  {:<{width}} {:>9}".format('#'+row['rank'], row['uname'], row['score'], width=uname_width))

def lookup_steamid(steamid, table_row):
    """add the username to the given row of the table

    Takes steamid (a numerical identifier)
    looks up and fetches the associated profile name
    adds it as a key-value pair in the row
    """
    url = 'http://steamcommunity.com/profiles/' + steamid + '/?xml=1'
    req = urllib.request.urlopen(url)
    xml_tree = ET.parse(req)
    root = xml_tree.getroot()
    uname = root.find('steamID').text
    # need conditional here because of some wierd problems with a certain user
    table_row['uname'] = "" if uname is None else uname

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
                        lookup_board('233610', val, int(opts.count), parseTime=timed)
                        # Flush print buffer after each board
                        print('', flush=True, end='')
                    else:
                        print('┌──────┬──────────────────────────────────┬──────────┐')
                        print('│{:^6}│ {:<33}│{:^9} │'.format('Rank', 'Player', 'Score' if timed else 'Score'))
                        print('├──────┼──────────────────────────────────┼──────────┤')
                        lookup_board('233610', val, int(opts.count), parseTime=timed)
                        # Flush print buffer after each board
                        print('└──────┴──────────────────────────────────┴──────────┘', flush=True)
                    break
