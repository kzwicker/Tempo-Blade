#!/bin/python
import json
import time
import os
import serial
import serial.tools.list_ports as listports
import pygame
"""
pygame.init()
res = (720,720) 
screen = pygame.display.set_mode(res) 
color = (255,255,255) 
color_light = (170,170,170) 
color_dark = (100,100,100) 
width = screen.get_width() 
height = screen.get_height() 
font = pygame.font.SysFont('Corbel',35)
"""

class Directions:
    up = 0
    down = 1
    left = 2
    right = 3
    upleft = 4
    upright = 5
    downleft = 6
    downright = 7
    any = 8

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
    def getEmoji(self):
        match self.direction:
            case Directions.up:
                return '🡑'
            case Directions.down:
                return '🡓'
            case Directions.left:
                return '🡐'
            case Directions.right:
                return '🡒'
            case Directions.upleft:
                return '🡔'
            case Directions.upright:
                return '🡕'
            case Directions.downleft:
                return '🡗'
            case Directions.downright:
                return '🡖'
            case Directions.any:
                return '•'

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
                outString += chr(note.getDirection())
            else:
                outString += ' '
        outString += '\n'
        for note in self.notesListLeft:
            if note is not None:
                outString += chr(note.getDirection())
            else:
                outString += ' '
        return outString

    def getDebug(self):
        outString = ""
        for i in range(0,16):
            outString += "|"
            if self.notesListLeft[i] is not None:
                outString += self.notesListLeft[i].getEmoji()
            else:
                outString += ' '
            if self.notesListRight[i] is not None:
                outString += self.notesListRight[i].getEmoji()
            else:
                outString += ' '
            outString += "|\n"
        return outString

# for use with the pygame version
class Arrow(pygame.sprite.Sprite):
    def __init__(self, note):
        super().__init__() self.note = note
        self.side = note.getColor()
        self.direction = note.getDirection()

    def loadArrow(self):
        if self.side == 0:
            arrSprite = pg.image.load('./Images/')
        else:
            arr

def main():
    global gameType
    gameType = chooseGameType()
    songFolder = chooseSong()
    difficultyName = chooseDifficulty(songFolder)
    port = choosePort()
    infoName, songName = getFilenames(songFolder)
    playGame(songName, getBPM(infoName), getNotes(difficultyName), port)

class gameTypes:
    terminal = 1
    serial = 2
    pygame = 3

def chooseGameType():
    print("Game types:")
    print("1: terminal")
    print("2: serial")
    print("3: pygame")
    try:
        num = int(input("Enter corresponding number to make a game selection: "))
    except:
        print("Please enter a number")
        quit()
    if num < 1 or num > 3:
        print("Invalid game choice")
        quit()
    return num

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

def sortDifficulty(file):
    if("Easy" in file):
        return 0
    if("Normal" in file):
        return 1
    if("Hard" in file):
        return 2
    if("Expert" in file):
        return 3
    if("ExpertPlus" in file):
        return 4
    
def chooseDifficulty(songFolder):
    difficultyFileList = []
    difficultyList = []
    for file in next(os.walk(songFolder))[2]:
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
            difficultyList.append(difficulty)
            difficultyFileList.append(file)
    difficultyList.sort(key=sortDifficulty)
    difficultyFileList.sort(key=sortDifficulty)
    for index, difficulty in enumerate(difficultyList):
        print(f"{index + 1}: {difficulty}")

    try:
        num = int(input("Enter corresponding number to make a difficulty selection: "))
    except:
        print("Please enter a number")
        quit()
    if (num < 1 or num > len(difficultyList)):
        print("Invalid song choice")
        quit()
    return f"{songFolder}/{difficultyFileList[num-1]}"

def choosePort():
    print("Available Ports:")
    comports = listports.comports()
    for index, port in enumerate(comports):
        print(f"{index}: {port.name} - {port.manufacturer}")
    try:
        num = int(input("Enter corresponding number to make a port selection or leave blank for debug: "))
    except:
        print("Port not specified, entering debug mode")
        return None
    if num < 0 or num >= len(comports):
        print("Invalid port choice")
        quit()
    return serial.Serial(comports[num].device, 115200)


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
            notesLabel = "_notes"
            if(notesJSON[notesLabel] == []):
                notesLabel = "_events"
            for note in notesJSON[notesLabel]:
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

def playGame(songFile, bpm, notesList, port):
    global gameType
    print(f"BPM: {bpm}")
    screen = ScreenState()
    noteIndex = 0
    leftNotes = []
    rightNotes = []
    running = False
    if gameType == gameTypes.terminal:
        print("\n" * 15)
    elif gameType == gameTypes.pygame:
        display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Tempo Blade')
        display.fill((0, 0, 0))
        pygame.display.flip()
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()
    pygame.mixer.music.load(songFile)
    pygame.mixer.music.play()
    startTime = time.time()
    for beat in range(int(notesList[len(notesList) - 1].getTime() + 18) * 4):
        # print screen to serial port or terminal
        if gameType == gameTypes.serial:
            port.write(bytes(screen.getScreen() + '\f', "utf-8"))
        if gameType == gameTypes.terminal:
            print(f"\033[16F{screen.getDebug()}", end="")
        if gameType == gameTypes.pygame:
            running = True
        while((time.time() - startTime) * bpm/60 <= (beat-15.25)/4):
            continue
        if(noteIndex >= len(notesList) or noteIndex < 0):
            screen.pushTwoNotes(None, None)
            continue
        while(notesList[noteIndex].getTime() <= beat/4):
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

def updatePygame

if __name__ == "__main__":
    main()
