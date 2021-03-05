import requests


# Make an API call and store the response
url = 'https://www.haloapi.com/stats/h5/players/EnduroCat14/matches'
headers = {'Ocp-Apim-Subscription-Key': 'f83454ddd4fb4e4da43f9752693bf8e2'}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")

# Store API response in a variable.
response_dict = r.json()
print(f"keys: {response_dict.keys()}")

# Explore information about the games
game_dicts = response_dict['Results']
print(f"Games returned: {len(game_dicts)}")

# Examine the first game
game_dict = game_dicts[0]
print(f"\nKeys:{len(game_dict)}")
for key in sorted(game_dict.keys()):
    print(key)


player_dict = game_dict['Players']
endurocat = player_dict[0]
for key in sorted(endurocat.keys()):
    print(key)
    

print(f"I GOT {endurocat['TotalKills']} KILLS!")
