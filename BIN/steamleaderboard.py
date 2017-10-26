#!/usr/bin/env python3

from optparse import OptionParser
from os import environ, get_terminal_size
from re import search
from threading import Thread
from unicodedata import  category
from urllib.request import urlopen
from xml.etree.ElementTree import parse as parse_tree

def terminal_size(fallback=(80, 24)):
    for i in range(0,3):
        try:
            columns, rows = get_terminal_size(i)
        except OSError:
            continue
        break
    else:  # set default if the loop completes which means all failed
        columns, rows = fallback

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
        "elevation": "1558823",
        "red heat": "2011155",
        "disassembly line": "2011156"
    },
    "stunt": {
        "credits": "1588771",
        "refraction": "1589164",
        "space skate": "1561263",
        "spooky town": "1573802",
        "stunt playground": "1561573",
        "tagtastic": "1572280",
        "neon park": "1952913"
    }
}
def get_key(path):
    """Gets your Steam web API key from the path provided."""
    return open(path, 'r').read(32)

def lookup_board(key, gameid, levelid, count, parsetime, table):
    """Look up a track on the steam leaderboard

    This function handles printing its data as well

    Takes a gameid, leaderboardid, count, and a table adds the top `count` entries
    in that leaderboard (calls lookup_steamid to get the profile name) to the table
    """
    url = 'http://steamcommunity.com/stats/' + gameid + '/leaderboards/' + levelid + '/?xml=1&start=1&end=' + str(count)
    # Make the request object
    req = urlopen(url)
    xml_tree = parse_tree(req)
    root = xml_tree.getroot()

    for entry in root.find('entries').findall('entry'):
        # get relavent data out of 'entry'
        rank = entry.find('rank').text
        steamid = entry.find('steamid').text
        score = entry.find('score').text
        if parsetime:
            minutes, milliseconds = divmod(int(score), 60000)
            seconds = float(milliseconds) / 1000
            score = "%i:%06.3f" % (minutes, seconds)
        table_row = {'rank' : rank, 'score' : score, 'steamid' : steamid}
        table.append(table_row)
    lookup_steamids(key, table)

def lookup_steamids(key, table):
    """Looks up a list of 64-bit steamids, makes an array of profile names

    Takes steamid (a numerical identifier)
    looks up and fetches the associated profile name
    """
    steamids = []
    for row in table:
        steamids.append(row['steamid'])
    url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=' + key + '&steamids=' + ','.join(steamids) + '&format=xml'
    req = urlopen(url)
    xml_tree = parse_tree(req)
    root = xml_tree.getroot()[0]
    for child in root:
        uname = child.find('personaname').text
        steamid = child.find('steamid').text
        for row in table:
            if row['steamid'] == steamid:
                row['uname'] = "" if uname is None else uname
                break
    return table

def nonspacing_count(s):
    """Counts the number of 'Nonspacing_Mark' characters in a string 's'"""
    count = 0
    for c in s:
        if category(c) == 'Mn':
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
parser.add_option("-f", "--key-file", action="store", default=(environ['HOME'] + "/.local/share/steamapikey"), dest="key_path", help="Path to Steam API key. ~/.local/steam/steamapikey by default")
parser.add_option("-k", "--key", action="store", dest="key", help="Steam API key")
(opts, args) = parser.parse_args()

# Main loop
threads = []
titles = []
tables = []
key = opts.key if opts.key else get_key(opts.key_path)

for mode, track_list in tracks.items():
    # limit mode to the mode requested
    if search(opts.mode.lower(), mode):
        for name, val in track_list.items():
            for arg in args:
                # limit tracks to tracks requested
                if search(arg.lower(), name):
                    timed = True
                    if mode == 'stunt':
                        timed = False
                    table = []
                    titles.append("\n{:^50}".format( name.title() + ": " + mode.title()))
                    new_thread = Thread(target = lookup_board, args = (key, '233610', val, int(opts.count), timed, table))
                    new_thread.start()
                    threads.append(new_thread)
                    tables.append(table)
                    break

# Print logic
for thread, title, table in zip(threads, titles, tables):
    # Print leaderboards as they are available
    thread.join()
    print(title)
    if(not opts.pretty):
        print('{:^6} {:<33} {:^9}'.format('Rank', 'Player', 'Score' if timed else 'Score'))
        for row in table:
            uname_width = 33 + nonspacing_count(row['uname'])
            print("{:>5}  {:<{width}} {:>9}".format('#'+row['rank'], row['uname'], row['score'], width=uname_width))
        # Flush print buffer after each board
        print('', flush=True, end='')
    else:
        print('┌──────┬──────────────────────────────────┬──────────┐')
        print('│{:^6}│ {:<33}│{:^9} │'.format('Rank', 'Player', 'Score' if timed else 'Score'))
        print('├──────┼──────────────────────────────────┼──────────┤')
        for row in table:
            uname_width = 33 + nonspacing_count(row['uname'])
            print("│{:>5} │ {:<{width}}│{:>9} │".format('#'+row['rank'], row['uname'], row['score'], width=uname_width))
        # Flush print buffer after each board
        print('└──────┴──────────────────────────────────┴──────────┘', flush=True)
