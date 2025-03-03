import zipfile
import os
import json
os.system("pip install requests")
import requests
url = "https://r2cdn.beatsaver.com/ced8a18aee94f77aa8b38ee10e5f2980d7f6c26b.zip"
filename = "starships.zip"
folder = "Songs/"
goofy = os.name == "nt"
r = requests.get(url, allow_redirects=True)
open(filename, 'wb').write(r.content)
with zipfile.ZipFile(filename, 'r') as zip_ref:
    info = json.load(zip_ref.open("info.dat"))
    if info["_version"] != "2.0.0":
        print("beatmap not version 2.0.0")
    folder += info["_songName"]
    zip_ref.extractall(folder)
os.remove(filename)