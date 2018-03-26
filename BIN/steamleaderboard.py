#!/usr/bin/env python3

from colored import attr
from optparse import OptionParser
from enum import Enum
from os import environ, get_terminal_size
from re import search
from threading import Thread
from urllib.request import urlopen
from defusedxml.ElementTree import parse as parse_tree
from matplotlib import pyplot, ticker

class Board:
    """board: Steam leaderboard from a given game id + board id

    displaytype: 1 for points, 2 for ???, 3 for time
    sortmethod: 1 for lowest best, 2 for highest best
    """
    def __init__(self, appid, lbid, title="", displaytype=3, sortmethod=1):
        self.displaytype = displaytype
        self.gameid = gameid
        self.lbid = lbid
        self.sortmethod = sortmethod
        self.title = title

    """GET the board's first `count` entries"""
    def fetch(self, count, apikey, usernames=True, steamiddb=None):
        return fetch_entries(self, 1, count, apikey, usernames=usernames)

    """GET the board's first entries between `start` and `end`"""
    def fetch_entries(self, start, end, apikey, usernames=True):
        url = 'http://steamcommunity.com/stats/' + appid + '/leaderboards/' + levelid + '/?xml=1&start=' + str(start) '&end=' + str(end)
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
        if usernames:
            lookup_steamids(self, api_key, steamiddb)

    def lookup_steamids(self, api_key, steamiddb):


    def add_steamids(self, api_key, steamiddb)

        def match_steamid(steamid, username, table):
            for row in table:
                if steamid == row['steamid']
                    row['uname'] = username
                    return True
            return False

        if steamiddb:
            for (sid, uname) in steamiddb:
                match_steamid(sid, uname, table)


    def print(self, style=3):
        pass

    """returns a list of Boards for this appid"""
    def get_boards(appid):
        boards = []
        url = 'http://steamcommunity.com/stats/' + appid + '/leaderboards?xml=1'
        # Make the request object
        req = urlopen(url)
        xml_tree = parse_tree(req)
        root = xml_tree.getroot()
        for board in root.find('leaderboard').findall('entry'):
            # get relavent data out of 'leaderboard'
            name = board.find('display_name')
            sortmethod = board.find('sortmethod')
            displaytype = board.find('displaytype')
            lbid = board.find('lbid')
            board = Board(appid, lbid, title=display_name,
                          sortmethod=sortmethod, displaytype=displaytype)
            boards.append(board)
        return boards

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

# UNUSED: Doesn't give mode, instead mode is part of
# <display_name> (e.g.: "Amusement (Sprint)")
# To adapt to any game, enable -g switch and use this
# function to get boards for any appid
def get_boards(api_key, appid):
    boards = []
    url = 'http://steamcommunity.com/stats/' + appid + '/leaderboards?xml=1'
    # Make the request object
    req = urlopen(url)
    xml_tree = parse_tree(req)
    root = xml_tree.getroot()
    for board in root.find('leaderboard').findall('entry'):
        # get relavent data out of 'leaderboard'
        name = board.find('display_name')
        lbid = board.find('lbid')
        is_timed = (board.find('sortmethod') == '2')
        board = {'name': name, 'id': lbid, 'is_timed': is_timed}
        boards.append(board)
    return boards

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

def lookup_board(api_key, appid, levelid, count, is_timed, table):
    """Look up a track on the steam leaderboard

    This function handles formatting its data as well

    Takes a appid, leaderboardid, count, and a table adds the top `count` entries
    in that leaderboard (calls lookup_steamid to get the profile name) to the table
    """
    url = 'http://steamcommunity.com/stats/' + appid + '/leaderboards/' + levelid + '/?xml=1&start=1&end=' + str(count)
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
    def lookup_group(dest_table, url):
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

    threads = []
    for i in range(0, len(table), MAX):
        steamids = []
        for row in table[i:i+MAX]:
            steamids.append(row['steamid'])
        url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=' + api_key + '&steamids=' + ','.join(steamids) + '&format=xml'
        new_thread = Thread(target = lookup_group, args = (table, url))
        new_thread.start()
        threads.append(new_thread)
    for thread in threads:
        thread.join()
    return table

# ==================
# MAIN program logic is here
# ==================

# Option parsing
parser = OptionParser()
parser.usage = "%prog level [level2 [...]] [options] (level is a regular expression)"
parser.add_option("-m", "--mode", action="store", default=".", dest="mode", help="Mode to lookup. Searches all by default")
# parser.add_option("-g","--game-id", action="store", default='233610', dest="appid", help="Game id to be used. Defaults to Distance. (You can try if you want.)")
parser.add_option("-n", "--number", action="store", default=15, dest="count", help="Number of places to print. Views top 15 by default")
parser.add_option("-s", "--simple", action="count", default=0, dest="strip", help="Disable pretty box drawings.  Repeat to strip column headings")
parser.add_option("-f", "--key-file", action="store", dest="api_key_path", help="Path to Steam API key. $XDG_DATA_HOME/steamapi/apikey by default")
parser.add_option("-p", "--plot", action="store_true", dest="plot", help="Plot the board instead.")
parser.add_option("-k", "--key", action="store", dest="api_key", help="Steam API key.  Overrides -f/--key-file")
(opts, args) = parser.parse_args()

# Get API key
api_key = opts.api_key
if not api_key:
    if opts.api_key_path:
        api_key = get_api_key(opts.api_key_path)
    else:
        try:
            api_key = get_api_key(environ['XDG_DATA_HOME'] + '/steamapi/apikey')
        except KeyError:
            api_key = get_api_key(environ['HOME'] + '/.local/share/steamapi/apikey')

# Lists to add
# TODO: change to one list
threads = []
titles = []
tables = []
timings = []
# ==============================
# Select maps and launch threads
# ==============================
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

# ======================
# Join threads and print
# ======================
for thread, title, table, is_timed in zip(threads, titles, tables, timings):
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
            print("{:>5}  {}\33[41G {:>9}".format('#'+row['rank'], row['uname'], row['score']))
        # Flush print buffer after each board
        print('', flush=True, end='')
    else:
        print('┌──────┬──────────────────────────────────┬──────────┐')
        print('│{:^6}│ {:<33}│{:^9} │'.format('Rank', 'Player', 'Score' if is_timed else 'Score'))
        print('├──────┼──────────────────────────────────┼──────────┤')
        for row in table:
            print("│{:>5} │ {}\33[43G│{:>9} │".format('#'+row['rank'], row['uname'], row['score']))
        # Flush print buffer after each board
        print('└──────┴──────────────────────────────────┴──────────┘', flush=True)
