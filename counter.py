# Program: counter.py
# Description: This program runs on an esp8266 board.  It makes requests to 
# the Halo 5 public API and uses the returned data to keep track of a 
# specified player's total kills.  This data is displayed via three digit
# seven segment display. 
#
# Last edit: March 14, 2020
# Author: Tyler Weir

import network
import urequests as requests
import time
import ujson as json
import machine

def do_connect():
    """Connect automatically to the Network."""
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Weir Farm 2.4GHz', 'bigchicken')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    return True

def callAPI():
    """Make a data request to the Halo5 public API."""
    url = "https://www.haloapi.com/stats/h5/players/MrFlyhigh/matches?include-times=True"
    key = {'Ocp-Apim-Subscription-Key': 'f83454ddd4fb4e4da43f9752693bf8e2'}

    print('Making an API Call')
    r = requests.get(url, headers=key)
    print(str(r.status_code))
    return r.json()

def toKillDateList(API_data):
    """Takes API data and returns a list of kills, date pairs for easy storage
       and processing."""
    stats = []
    
    game_dicts = API_data['Results']
    for i in range(len(game_dicts)):
       match_dict = game_dicts[i]   # Access the ith game

       player_dict = game_dict['Players']   # Access the players data
       player = player_dict[0]              # Access only the first player
       num_kills = player['TotalKills']     # Record the player's kills

       date_dict = game_dict['MatchCompletedDate']  # Access the game date
       game_date = date_dict['ISO8601Date']
       
       stats.append((num_kills, game_date))

    return stats

def saveData(stats):
    """Save the data in a json file."""
    filename = 'backup.json'
    with open(filename, 'w') as f:
        json.dump(stats, f)

def loadData():
    """Load backed up data from a json file."""
    filename = 'backup.json'
    with open(filename) as f:
        stats = json.load(f)
        return stats

def toggle(p):
    p.value(not p.value())

def run():
    # Connect to the internet
    do_connect()

    # Make a request to the API and turn it to list kill date pairs
    gameHistory = callAPI()
    stats = toKillDateList(gameHistory) 
    print(stats) 
    
    saveData(stats)

if __name__ == '__main__':
    run()
