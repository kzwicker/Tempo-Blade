#!/bin/python
import json
import time
import os
import serial
import subprocess

class Note: 
    def __init__(self, time, color, direction):
        self.time = time
        self.color = color # 0 = left, 1 = right
        self.direction = direction

    def getTime(self):
        return self.time

    def getColor(self):
        return self.color

    def getDirection(self):
        return self.direction

class ScreenState:
    def __init__(self):
        self.notesListLeft = [None] * 16
        self.notesListRight = [None] * 16

    def pushTwoNotes(self, Lnote, Rnote):
        self.notesListLeft.insert(0, Lnote)
        self.notesListRight.insert(0, Rnote)
        self.notesListLeft.pop()
        self.notesListRight.pop()

    def getScreen(self):
        outString = ""
        for note in self.notesListRight:
            if note is not None:
                outString += str(note.getDirection())
            else:
                outString += '-'
        outString += '\n'
        for note in self.notesListLeft:
            if note is not None:
                outString += str(note.getDirection())
            else:
                outString += '-'
        
        return outString
            



def main():
    songFolder = chooseSong()
    difficultyName = chooseDifficulty(songFolder)
    infoName, songName = getFilenames(songFolder)
    playGame(songName, getBPM(infoName), getNotes(difficultyName))

def chooseSong():
    if not os.path.isdir("./Songs"):
        print("No song files found!")
        quit()
    print("Available Songs:")
    songList = next(os.walk('./Songs'))[1]
    for index, song in enumerate(songList):
        print(f"{index + 1}: {song}")
    try:
        num = int(input("Enter corresponding number to make a song selection: "))
    except:
        print("Please enter a number")
        quit()
    if(num < 1 or num > len(songList)):
        print("Invalid song choice")
        quit()
    checkFolder(f"./Songs/{songList[num - 1]}")
    return f"./Songs/{songList[num - 1]}"

def chooseDifficulty(songFolder):
    print("Available Difficulties:")
    difficultyList = []
    index = 1
    for file in next(os.walk(songFolder))[2]:
        #if(fileName != "info" and fileName != "Info" and fileName != "song" and fileName != "cover"):
        difficulty = ""
        if("Easy" in file):
            difficulty = "Easy"
        if("Normal" in file):
            difficulty = "Normal"
        if("Hard" in file):
            difficulty = "Hard"
        if("Expert" in file):
            difficulty = "Expert"
        if("ExpertPlus" in file):
            difficulty = "Expert+"
        if(difficulty != ""):
            print(f"{index}: {difficulty}")
            index += 1
            difficultyList.append(file)
    try:
        num = int(input("Enter corresponding number to make a difficulty selection: "))
    except:
        print("Please enter a number")
        quit()
    if (num < 1 or num > len(difficultyList)):
        print("Invalid song choice")
        quit()
    return f"{songFolder}/{difficultyList[num-1]}"

def checkFolder(folderPath):
    if not os.path.isdir(folderPath):
        print("Folder does not exist! Please enter a valid folder name!")
        quit()
    fileList = next(os.walk(folderPath))[2]
    songFileFound = False
    difficultyFound = False
    for file in fileList:
        if(file[file.find("."):] == ".egg"):
            songFileFound = True
        if("Easy" in file or "Normal" in file or "Hard" in file or "Expert" in file or "ExpertPlus" in file):
            difficultyFound = True
    if not ("info.dat" in fileList or "Info.dat" in fileList) or not songFileFound or not difficultyFound:
        print("Song files missing!")
        quit()

def getFilenames(folderPath):
    infoName = f"{folderPath}/info.dat"
    if os.path.exists(f"{folderPath}/Info.dat"):
        infoName = f"{folderPath}/Info.dat"
    songFileName = ""
    for file in next(os.walk(folderPath))[2]:
        if(file[file.find("."):] == ".egg"):
            songFileName = file
    return infoName, f"{folderPath}/{songFileName}"

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
    #scale by 4 seconds total
    songDelay = int(16 * 60/bpm)
    command = ""
    if(os.name == "nt"):
        command = f"timeout /t {songDelay} > NUL"
    else:
        command = f"sleep {songDelay}"
    command += f" && ffplay -autoexit -nodisp -loglevel error \"{songFile}\""
    #subprocess.Popen(["ffplay", "-autoexit", "-nodisp", "-loglevel", "error", songFile])
    subprocess.Popen(command, shell=True)
    print(f"BPM: {bpm}")
    screen = ScreenState()
    startTime = time.time()
    #update this later, probably high due to printing
    loop_start = time.time()
    delay = 0
    noteIndex = 0
    leftNotes = []
    rightNotes = []
    print("\n\n\n\n\n")
    for beat in range(int(notesList[len(notesList) - 1].getTime() + 18)):
        print(f"\033[F\033[F\033[F\033[F\033[F________________\n{screen.getScreen()}\n________________")
        #this correction lol
        print(f"Accumulated delay: {delay}")
        delay += time.time()-loop_start + 0.0035 #magic number from trial and error
        while((time.time() - startTime - delay) * bpm/60 < beat):
            continue
        loop_start = time.time()
        if(noteIndex >= len(notesList) or noteIndex < 0):
            screen.pushTwoNotes(None, None)
            #print(f"\033[F\033[F\033[F\033[F________________\n{screen.getScreen()}\n________________")
            continue
        while(notesList[noteIndex].getTime() <= beat):
            #print(f"{beat}: {notesList[noteIndex]}")
            if(notesList[noteIndex].getColor() == 0):
                leftNotes.append(notesList[noteIndex])
            else:
                rightNotes.append(notesList[noteIndex])
            noteIndex += 1
            if(noteIndex >= len(notesList)):
                break
        if(len(leftNotes) + len(rightNotes) == 0):
            screen.pushTwoNotes(None, None)
        while(len(leftNotes) > 0 and len(rightNotes) > 0):
            screen.pushTwoNotes(leftNotes[0], rightNotes[0])
            leftNotes.pop(0)
            rightNotes.pop(0)
        while(len(leftNotes) > 0):
            screen.pushTwoNotes(leftNotes[0], None)
            leftNotes.pop(0)
        while(len(rightNotes) > 0):
            screen.pushTwoNotes(None, rightNotes[0])
            rightNotes.pop(0)
"""
    for index, note in enumerate(notesList):
        while(time.time() - startTime - delay < (note.getTime()) * 60/bpm):
            continue
        if note.getColor() == 0 and leftNote == None:
            leftNote = notesList[noteIndex]
        elif rightNote == None:
            rightNote = notesList[noteIndex]
        if time.time() - startTime - delay > (note.time) * 60/bpm:
            screen.pushTwoNotes(leftNote, rightNote)
            leftNote = None
            rightNote = None
        print(f"{note.getColor()}, {note.getDirection()}")
"""    
        
"""
    while noteIndex < len(notesList):
        leftNote = None
        rightNote = None
        while (time.time() - startTime - delay) < (notesList[noteIndex].time - 4) * 60/bpm:
            print(noteIndex)
            if notesList[noteIndex].getColor() == 0 and leftNote == None:
                leftNote = notesList[noteIndex]
            elif rightNote == None:
                rightNote = notesList[noteIndex]
            noteIndex += 1
            if noteIndex >= len(notesList):
                break

        screen.pushTwoNotes(leftNote, rightNote)
        #print(f"{screen.getScreen()}")
"""

if __name__ == "__main__":
    main()