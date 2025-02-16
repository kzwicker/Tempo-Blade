#!/bin/python
import json
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
    songFolder = chooseSong()
    infoName, difficultyName, songName = getFilenames(songFolder)
    playGame(songName, getBPM(infoName), getNotes(difficultyName))

def chooseSong():
    if not os.path.isdir("./Songs"):
        print("No song files found!")
        quit()
    print("Available Songs:")
    songList = next(os.walk('./Songs'))[1]
    for index, song in enumerate(songList):
        print(f"{index + 1}: {song}")
    num = int(input("Enter corresponding number to make a song selection: "))
    if(num < 1 or num > len(songList)):
        print("Invalid song choice")
        quit()
    checkFolder(f"./Songs/{songList[num - 1]}")
    return f"./Songs/{songList[num - 1]}"

def checkFolder(folderPath):
    if not os.path.isdir(folderPath):
        print("Folder does not exist! Please enter a valid folder name!")
        quit()
    if not (os.path.exists(f"{folderPath}/info.dat") or os.path.exists(f"{folderPath}/Info.dat")) or not os.path.exists(f"{folderPath}/Normal.dat") or not os.path.exists(f"{folderPath}/song.egg"):
        print("Song files missing!")
        quit()

def getFilenames(folderPath):
    infoName = f"{folderPath}/info.dat"
    if os.path.exists(f"{folderPath}/Info.dat"):
        infoName = f"{folderPath}/Info.dat"
    return infoName, f"{folderPath}/Normal.dat", f"{folderPath}/song.egg"

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
        while (time.time() - startTime) < (note.time - 10):
            continue
        #last values in print can be removed
        print(f"{note.getColor()}, {note.getDirection()}, {note.time}, {time.time()-startTime}")

if __name__ == "__main__":
    main()
