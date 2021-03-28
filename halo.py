import time
import json
import requests
import iso8601
import datetime
import threading
from pytz import timezone

# Global API information
gamertag = 'MrFlyhigh'    
url = f"https://www.haloapi.com/stats/h5/players/{gamertag}/matches?include-times=True"
headers = {'Ocp-Apim-Subscription-Key': 'f83454ddd4fb4e4da43f9752693bf8e2'}

# Global variables for threads to access
games = []
count = 0

class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print(f"Starting {self.name}")
        displayCount(self.name)

def callAPI():
    """Calls the API and returns the result in json format."""
    r = requests.get(url, headers=headers)
    print(f"Status code: {r.status_code}")

    return r.json()

def toKillDateList(API_data):
    """Takes API data and returns a list of (kills, date) pairs for easy storage."""
    stats = []

    game_dicts = API_data['Results']        # Access the results key
    for i in range(len(game_dicts)):
        game_dict = game_dicts[i]           # Access the ith game

        player_dict = game_dict['Players']  # Access the players data
        player = player_dict[0]             # Access only the first player
        num_kills = player['TotalKills']    # Record the player's kills

        id_dict = game_dict['Id']
        game_id = id_dict['MatchId']

        date_dict = game_dict['MatchCompletedDate'] # Access the game date
        game_date = date_dict['ISO8601Date']
        game_date_UTC = iso8601.parse_date(game_date)   # Parse the iso8601 date
        game_date_PAC = game_date_UTC.astimezone(timezone('US/Pacific'))    # Change to Pacific timezone
        
        stats.append((num_kills, game_id, game_date_PAC.strftime('%m-%d')))

    return stats

def getTodaysGames():
    """Gets todays game history from the API."""
    api_data = callAPI()
    gameHistory = toKillDateList(api_data) 
    todaysDate = datetime.date.today().strftime("%m-%d") 
    todaysGames = [(k, i, d) for (k, i, d) in gameHistory if d == todaysDate]

    return todaysGames

def writeBackup(games):
    filename = 'games.json'
    with open(filename, 'w') as f:
        json.dump(games, f)

def readBackup():
    filename = 'games.json'
    try:
        with open(filename) as f:
            games = json.load(f)
        return games
    except FileNotFoundError:
        return []

def containsID(games, ID):
    for game in games:
        if game[1] == ID:
            return True
    return False

def displayCount(threadName):
    while True:
        print(f"{threadName} says:")
        print(f"Total spartans bested: {count}")
        time.sleep(5)

if __name__ == '__main__':
    todaysDate = datetime.date.today().strftime("%m-%d") 

    # Reference the backup in case games were lost because of power outage
    backUp = readBackup()
    for game in backUp:
        if game[2] == todaysDate:
            print("Adding a game from backup.")
            games.append(game)
            count+=game[0]
    
    # Spin up the display thread
    displayThread = myThread(1, "Display Thread")
    displayThread.start()

    # Enter the main program loop
    while True:
        print("Calling API")
        todaysGames = getTodaysGames()  # Get todays games from the API
        for game in todaysGames:        # Add new games to the list
            if not containsID(games, game[1]):
                print("Adding a game to the count.")
                games.append(game)
                count+=game[0]    
        
        if len(games) >= 25:            # Make a backup if there are more than 25 games
            writeBackup(games)
        
        # Restart counts and clear backup if it is a new day
        currentDate = datetime.date.today().strftime("%m-%d")
        if currentDate != todaysDate:
            writeBackup([])
            games = []
            count = 0
            todaysDate = currentDate
        
        # Wait 10 seconds before next API call
        time.sleep(10)
