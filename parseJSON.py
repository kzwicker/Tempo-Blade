#!/bin/python
import json
import sys
import time
import os
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
    folderName = getFolder(sys.argv[1])

    infoName = folderName + "/" + sys.argv[2] + ".dat"
    difficultyName = folderName + "/" + sys.argv[3] + ".dat"
    songName = folderName + "/" + sys.argv[4] + ".egg"

    bpm = getBPM(infoName)
    notesList = getNotes(difficultyName)
    playGame(songName, bpm, notesList)

def checkArgs(arguments):
    if len(arguments) != 5:
        print("Bad arguments")
        print("usage: ./parseJSON.py <folderName> <Info/info> <Difficulty> <songFileName>")
        quit()

def getFolder(folderName):
    folderRoot = os.getcwd() + "/" + folderName
    if os.path.isdir(folderRoot) == False:
        print(f"Folder does not exist! Please enter a valid folder name!")
        quit()
    return folderRoot

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
        while (time.time() - startTime) * bpm/60 < (note.time - 4*bpm/60):
            continue
        print(f"{note.getColor()}, {note.getDirection()}")

if __name__ == "__main__":
    main()
