#!/usr/bin/env python3

from colored import attr, bg
from optparse import OptionParser
from os import environ, get_terminal_size
from re import search
from threading import Thread
from unicodedata import  category
from urllib.request import urlopen
from xml.etree.ElementTree import parse as parse_tree
from matplotlib import pyplot, ticker

# terminal_size is not being used right now,
# but I might later to set table width or print tables side-by-side
def terminal_size():
    if isatty(1):
        try:
            columns, rows = get_terminal_size(1)
        except OSError:
            return False
        return (columns, rows)
    return False



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

def format_time(score, *_):
    minutes, milliseconds = divmod(int(score), 60000)
    seconds = float(milliseconds) / 1000
    return "%i:%06.3f" % (minutes, seconds)


def plot_board(table, title, is_timed):
    xs = []
    ys = []
    for row in table:
        xs.append(int(row['rank']))
        ys.append(int(row['score']))
    fig = pyplot.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    if is_timed:
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    ax.yaxis.grid(which='major', lw='1')
    ax.plot(xs, ys)
    ax.set_title(title)
    fig.savefig('{}.png'.format(title))

def get_api_key(path):
    """Gets your Steam web API key from the path provided."""
    return open(path, 'r').read(32)

def lookup_board(api_key, gameid, levelid, count, is_timed, table):
    """Look up a track on the steam leaderboard

    This function handles formatting its data as well

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
        if is_timed:
            score = format_time(score)
        table_row = {'rank' : rank, 'score' : score, 'steamid' : steamid}
        table.append(table_row)
    if not opts.plot:
        lookup_steamids(api_key, table)

def lookup_steamids(api_key, table):
    """Looks up a list of 64-bit steamids, makes an array of profile names

    Takes steamid (a numerical identifier)
    looks up and fetches the associated profile name

    Max steamid count per lookup is 100
    """
    MAX = 100
    for i in range(0, len(table), MAX):
        steamids = []
        for row in table[i:i+MAX]:
            steamids.append(row['steamid'])
        url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=' + api_key + '&steamids=' + ','.join(steamids) + '&format=xml'
        request = urlopen(url)
        xml_tree = parse_tree(request)
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
parser.add_option("-s", "--simple", action="count", default=0, dest="strip", help="Disable pretty box drawings.  Repeat to strip column headings")
parser.add_option("-f", "--key-file", action="store", dest="api_key_path", help="Path to Steam API key. $XDG_DATA_HOME/steamapi/apikey by default")
parser.add_option("-p", "--plot", action="store_true", dest="plot", help="Plot the board instead.")
parser.add_option("-k", "--key", action="store", dest="api_key", help="Steam API key.  Overrides -f/--key-file")
(opts, args) = parser.parse_args()

# Main loop
threads = []
titles = []
tables = []
timings = []
api_key = opts.api_key
if not api_key:
    if opts.api_key_path:
        api_key = get_api_key(opts.api_key_path)
    else:
        try:
            api_key = get_api_key(environ['XDG_DATA_HOME'] + '/steamapi/apikey')
        except:
            api_key = get_api_key(environ['HOME'] + '/.local/share/steamapi/apikey')

for mode, track_list in tracks.items():
    # limit mode to the mode requested
    if search(opts.mode.lower(), mode):
        for name, val in track_list.items():
            for arg in args:
                # limit tracks to tracks requested
                if search(arg.lower(), name):
                    is_timed = True
                    if mode == 'stunt':
                        is_timed = False
                    timings.append(is_timed)
                    table = []
                    if opts.plot:
                        is_timed = False
                    titles.append(name.title() + ": " + mode.title())
                    new_thread = Thread(target = lookup_board, args = (api_key, '233610', val, int(opts.count), is_timed, table))
                    new_thread.start()
                    threads.append(new_thread)
                    tables.append(table)
                    break

# Print logic
for thread, title, table, is_timed in zip(threads, titles, tables, timings):
    # Print leaderboards as they are available
    thread.join()
    if opts.plot:
        plot_board(table, title, is_timed)
        continue
    title = '{:^50}'.format(title)
    if opts.strip < 2:
        print()
    if opts.strip < 3:
        print("{}{}{}".format(attr(1), title, attr(0)))
    else:
        print(title)
    if opts.strip > 0:
        if opts.strip == 1:
            print(' {}{:^5} {:<33} {:^9}{}'.format(attr(4), 'Rank', 'Player', 'Score' if is_timed else 'Score', attr(0)))
        for row in table:
            uname_width = 33 + nonspacing_count(row['uname'])
            print("{:>5}  {:<{width}} {:>9}".format('#'+row['rank'], row['uname'], row['score'], width=uname_width))
        # Flush print buffer after each board
        print('', flush=True, end='')
    else:
        print('┌──────┬──────────────────────────────────┬──────────┐')
        print('│{:^6}│ {:<33}│{:^9} │'.format('Rank', 'Player', 'Score' if is_timed else 'Score'))
        print('├──────┼──────────────────────────────────┼──────────┤')
        for row in table:
            uname_width = 33 + nonspacing_count(row['uname'])
            print("│{:>5} │ {:<{width}}│{:>9} │".format('#'+row['rank'], row['uname'], row['score'], width=uname_width))
        # Flush print buffer after each board
        print('└──────┴──────────────────────────────────┴──────────┘', flush=True)
