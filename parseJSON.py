#!/bin/python
import json
import sys
import time
import subprocess

class Note: 
    def __init__(self, time, color, direction):
        self.time = time
        self.color = color
        self.direction = direction

    def getTime(self):
        return self.time

    def getColor(self):
        return self.color

    def getDirection(self):
        return self.direction


fileName = None
fileParsed = False

bpm = 0

if len(sys.argv) < 4:
    print("Bad arguments")
    print("usage: ./parseJSON.py <Info.dat> <Beatmap.dat> <Song.egg>")
    quit()

with open(sys.argv[1]) as infoFile:
    info = json.load(infoFile)
    if info["_version"] != "2.0.0":
        print("beatmap not version 2.0.0")
        quit()
    bpm = info["_beatsPerMinute"]
    fileParsed = True
if not fileParsed:
    print(f"Failed to parse {sys.argv[1]}")
    quit()

notesList = []
direction = 0

fileParsed = False
with open(sys.argv[2]) as notesFile:
    notesJSON = json.load(notesFile)
    if "_BPMChanges" in notesJSON and notesJSON["_BPMChanges"] != []:
        print("beatmap contains BPM changes")
        quit()
    for note in notesJSON["_notes"]:
        direction = 8
        if "_cutDirection" in note:
            direction = note["_cutDirection"]
        elif "_value" in note:
            direction = note["_value"]
        notesList.append(Note(note["_time"], note["_type"], direction))
    fileParsed = True
if not fileParsed:
    print(f"Failed to parse {sys.argv[2]}")
    quit()


subprocess.Popen(["ffplay", "-autoexit", "-nodisp", "-loglevel", "error", sys.argv[3]])
startTime = time.time()
print(f"BPM: {bpm}")
for note in notesList:
    while (time.time() - startTime) * bpm/60 < note.time:
        continue
    print(f"{note.getColor()}, {note.getDirection()}")
