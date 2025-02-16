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

def main():
    checkArgs(sys.argv)
    bpm = getBPM(sys.argv[1])
    notesList = getNotes(sys.argv[2])
    playGame(sys.argv[3], bpm, notesList)

def checkArgs(arguments):
    if len(arguments) != 4:
        print("Bad arguments")
        print("usage: ./parseJSON.py <Info.dat> <Beatmap.dat> <Song.egg>")
        quit()

def getBPM(fileName):
    try:
        with open(fileName) as infoFile:
            info = json.load(infoFile)
            if info["_version"] != "2.0.0":
                print("beatmap not version 2.0.0")
                quit()
            return info["_beatsPerMinute"]
    except:
        print(f"Failed to parse {fileName}")
        quit()

def getNotes(fileName):
    try:
        with open(fileName) as notesFile:
            notesJSON = json.load(notesFile)
            if "_BPMChanges" in notesJSON and notesJSON["_BPMChanges"] != []:
                print("beatmap contains BPM changes")
                quit()
            direction = 0
            notesList = []
            for note in notesJSON["_notes"]:
                direction = 8
                if "_cutDirection" in note:
                    direction = note["_cutDirection"]
                elif "_value" in note:
                    direction = note["_value"]
                notesList.append(Note(note["_time"], note["_type"], direction))
            return notesList
    except:
        print(f"Failed to parse {fileName}")
        quit()

def playGame(songFile, bpm, notesList):
    subprocess.Popen(["ffplay", "-autoexit", "-nodisp", "-loglevel", "error", songFile])
    startTime = time.time()
    print(f"BPM: {bpm}")
    for note in notesList:
        while (time.time() - startTime) * bpm/60 < note.time:
            continue
        print(f"{note.getColor()}, {note.getDirection()}")

if __name__ == "__main__":
    main()