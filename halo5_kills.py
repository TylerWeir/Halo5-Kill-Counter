import requests


# Make an API call and store the response
url = 'https://www.haloapi.com/stats/h5/players/MrFlyhigh/matches'
headers = {'Ocp-Apim-Subscription-Key': 'f83454ddd4fb4e4da43f9752693bf8e2'}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")

# Store API response in a variable.
response_dict = r.json()

# Explore information about the games
game_dicts = response_dict['Results']

for i in range(len(game_dicts)):
    game_dict = game_dicts[i]   # Examine the ith game
    player_dict = game_dict['Players']
    endurocat = player_dict[0]
    print(f"Game {i+1}: \tKills: {endurocat['TotalKills']} 
                        \tDeaths: {endurocat['TotalDeaths']} 
                        \tKD: {endurocat['TotalKills']/endurocat['TotalDeaths']}")        

