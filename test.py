import zipfile
import os
import json
import requests
song = input("Enter song: ")
request = f"https://api.beatsaver.com/search/text/0?leaderboard=All&pageSize=20&q={song}"
page_source = requests.get(request).text.encode("utf-8")
filename = "website.json"
open(filename, 'wb').write(page_source)
songs = json.loads(page_source)

url = songs["docs"][0]["versions"][0]["downloadURL"]
filename = "starships.zip"
folder = "Songs/"
r = requests.get(url, allow_redirects=True)
open(filename, 'wb').write(r.content)
with zipfile.ZipFile(filename, 'r') as zip_ref:
    info = json.load(zip_ref.open("info.dat"))
    if info["_version"] != "2.0.0":
        print("beatmap not version 2.0.0")
    folder += info['_songName']
    folder = folder.replace("'", "").replace("\"", "")
    zip_ref.extractall(folder)
os.remove(filename)