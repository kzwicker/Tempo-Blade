import requests
import json
song = input("Enter song: ")
url = f"https://api.beatsaver.com/search/text/0?leaderboard=All&pageSize=20&q={song}"
page_source = requests.get(url).text.encode("utf-8")
filename = "website.json"
open(filename, 'wb').write(page_source)
songs = json.loads(page_source)
print(songs["docs"][0]["versions"][0]["downloadURL"])