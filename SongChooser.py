import zipfile
import os
import json
import requests
song = input("Enter song: ")
request = f"https://api.beatsaver.com/search/text/0?leaderboard=All&pageSize=20&q={song}"
page_source = requests.get(request).text.encode("utf-8")
#filename = "website.json"
#open(filename, 'wb').write(page_source)
songs = json.loads(page_source)
choice = 0
print()
for x in range(len(songs["docs"]) - 1):
    print(f"{x + 1}: ")
    print(songs["docs"][x]["name"])
    print(f"Uploaded by {songs["docs"][x]["uploader"]["name"]}\n")
choice = int(input("Enter song choice (anything outside will default to 1): "))
if(choice > len(songs["docs"]) or choice < 1):
    choice = 0
url = songs["docs"][choice - 1]["versions"][0]["downloadURL"]
filename = "_garbage.zip"
folder = "Songs/"
r = requests.get(url, allow_redirects=True)
open(filename, 'wb').write(r.content)
with zipfile.ZipFile(filename) as zip_ref:
    info = json.load(zip_ref.open("info.dat"))
    if info["_version"] != "2.0.0":
        print("beatmap not version 2.0.0")
    folder += info['_songName']
    folder = folder.replace("'", "").replace("\"", "")
    zip_ref.extractall(folder)
os.remove(filename)