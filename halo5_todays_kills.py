# This program makes periodic requests to the Halo 5 public API and uses the 
# returned data to keep track of today's total kills. This data is displayed
# via the output pins on a raspberry pi.
#
# By: Tyler Weir

import requests
import iso8601
import datetime
from pytz import timezone

class KillCounter:
    """Track the today's total Halo 5 kills."""

    def __init__(self, gamertag):
        self.url = f"https://www.haloapi.com/stats/h5/players/{gamertag}/matches?include-times=True"
        self.headers = {'Ocp-Apim-Subscription-Key': 'f83454ddd4fb4e4da43f9752693bf8e2'}          
        
        self.records = []   # used to store the daily data, will be replaced with a json

    def callAPI(self):
        """Calls the API and returns the result in json format."""
        r = requests.get(self.url, headers=self.headers)
        print(f"Status code: {r.status_code}")

        return r.json()
    
    def toKillDateList(self, API_data):
        """Takes API data and returns a list of (kills, date) pairs for easy 
           storage."""
        stats = [] 
         
        game_dicts = API_data['Results']         # Access the results key
        for i in range(len(game_dicts)):
            game_dict = game_dicts[i]            # Access the ith game
            
            player_dict = game_dict['Players']   # Access the players data
            player = player_dict[0]              # Access only the first player
            num_kills = player['TotalKills']     # Record the player's kills

            date_dict = game_dict['MatchCompletedDate'] # Access the game date
            game_date = date_dict['ISO8601Date']
            game_date_UTC = iso8601.parse_date(game_date)   # Parse the iso date
            game_date_PAC = game_date_UTC.astimezone(timezone('US/Pacific')) # Change to pacific time 

            # Now get the game id number

            print(f"Date: {game_date_PAC.strftime('%m-%d %H:%M')} \tGame {i+1}: \tKills: {player['TotalKills']} \tDeaths: {player['TotalDeaths']} \tKD: {player['TotalKills']/player['TotalDeaths']}")          
            stats.append((num_kills, game_date_PAC))

        #print(stats)
                
            
if __name__ == '__main__':
    kill_counter = KillCounter("EnduroCat14")

    api_data = kill_counter.callAPI()
    kill_counter.toKillDateList(api_data)
