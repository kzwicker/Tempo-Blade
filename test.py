import requests
import zipfile
import os
import json
url = "https://r2cdn.beatsaver.com/ced8a18aee94f77aa8b38ee10e5f2980d7f6c26b.zip"
filename = "starships.zip"
folder = "Songs/"
goofy = os.name == "nt"
r = requests.get(url, allow_redirects=True)
open(filename, 'wb').write(r.content)
with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall("FOLDER")
with open("FOLDER/info.dat") as infoFile:
    info = json.load(infoFile)
    if info["_version"] != "2.0.0":
        print("beatmap not version 2.0.0")
    folder += info["_songName"]
if os.path.exists(folder):
    command = f"rm -rf {folder}"
    if(goofy):
        command = f"powershell -command '{command}' > NULL"
    os.system(command)
command = f"mv FOLDER {folder}"
if(goofy):
    command = f"powershell -command '{command}' > NULL"
os.system(command)
os.remove(filename)