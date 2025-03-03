import requests
import json
song = input("Enter song: ")
url = f"https://api.beatsaver.com/search/text/0?leaderboard=All&pageSize=20&q={song}"
page_source = requests.get(url).text.encode("utf-8")
filename = "website"
open(filename, 'wb').write(page_source)
with open(filename) as songsFile:
    songs = json.load(songsFile)
    print(songs)