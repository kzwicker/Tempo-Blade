#!/bin/python
import json
import time
import os
import serial
import serial.tools.list_ports as listports
import requests
import zipfile
import shutil
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
"""
pygame.init()
screenWidth = 720
screenHeight = 720
screen = pygame.display.set_mode([screenWidth, screenHeight]) 
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

    def pushTwoNotes(self, Lnote, Rnote, port):
        self.notesListLeft.insert(0, Lnote)
        self.notesListRight.insert(0, Rnote)
        playedL = self.notesListLeft.pop()
        playedR = self.notesListRight.pop()
        if(port == None):
            return
        if(playedL == None):
            ch1 = ' '
        else:
            ch1 = chr(playedL.getDirection())
        if(playedR == None):
            ch2 = ' '
        else:
            ch2 = chr(playedR.getDirection())
        port.write(bytes(f"h{ch1}{ch2}", "utf-8"))

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
    def __init__(self, note, gameScreen):
        pygame.sprite.Sprite.__init__(self)
        self.note = note
        self.side = note.getColor()
        self.direction = note.getDirection()
        self.y = -193 ## height of image --> 193px
        self.x = 0 ## arbitrary num
        self.moveBy = 636/16
        self.loadArrow()

    def loadArrow(self):
        if self.side == 0:
            self.imageName = "./Images/fallingLeftArr"
            self.x = 260
        else:
            self.imageName = "./Images/fallingRightArr"
            self.x = 470

        if self.direction == Directions.down:
            self.imageName += "180.png"
        elif self.direction == Directions.left:
            self.imageName += "90.png"
        elif self.direction == Directions.right:
            self.imageName += "270.png"
        elif self.direction == Directions.upleft:
            self.imageName += "45.png"
        elif self.direction == Directions.downleft:
            self.imageName += "135.png"
        elif self.direction == Directions.downright:
            self.imageName += "225.png"
        elif self.direction == Directions.upright:
            self.imageName += "315.png"
        else:
            self.imageName += "0.png"
        
        self.image = pygame.image.load(self.imageName).convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    ## in main game func --> create list of notes and iterate through all to update all
    ## delete notes when hit/off screen in that list
    def updatePos(self):
        self.y += self.moveBy
        self.rect.center = (self.x, self.y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def offScreen(self):
        if self.y >= 800:
            return True
        else:
            return False 

def main():
    pygame.mixer.init() ## this could be leading to slow down! move this down to the loop if so
    returnNlinesUp(1)
    stayInMenu = True
    while(stayInMenu):
        print("1: Search for and add a new song")
        print("2: Edit saved songs")
        print("Anything else: Begin song selection and play game")
        try:
            match(input()):
                case "1":
                    returnNlinesUp(4)
                    loadNewSong()
                case "2":
                    returnNlinesUp(4)
                    editSongs()
                case _:
                    returnNlinesUp(3)
                    stayInMenu = False
        except KeyboardInterrupt:
            quit()
    returnNlinesUp(1)
    global gameType
    gameType, songFolder, difficultyName, port, infoName, songName = [None] * 6
    gameType = chooseGameType()
    songFolder = chooseSong()
    difficultyName = chooseDifficulty(songFolder)
    port = choosePort()
    infoName, songName = getFilenames(songFolder)
    try:
        playGame(songName, getBPM(infoName), getNotes(difficultyName), port)
    except KeyboardInterrupt:
        quit()

class gameTypes:
    terminal = 1
    serial = 2
    pygame = 3

def editSongs():
    if not os.path.isdir("./Songs"):
        print("No song files found!")
        quit()
    print("Available Songs:")
    prompt = "Enter corresponding number to delete, anything else to return to menu: "
    while(True):
        lines = 0
        songList = next(os.walk('./Songs'))[1]
        for index, song in enumerate(songList):
            print(f"{index + 1}: {song}")
            lines += 1
        try:
            lines += 1
            num = int(input(prompt))
        except KeyboardInterrupt:
            quit()
        except:
            returnNlinesUp(lines + 1)
            return
        if(num < 1 or num > len(songList)):
            returnNlinesUp(1)
            prompt = "Please enter a valid number: "
            continue
        else:
            returnNlinesUp(lines)
            shutil.rmtree(f"./Songs/{songList[num-1]}")

def loadNewSong():
    song = input("Enter song: ")
    lines = 1
    request = f"https://api.beatsaver.com/search/text/0?leaderboard=All&pageSize=20&q={song}"
    page_source = requests.get(request).text.encode("utf-8")
    songs = json.loads(page_source)
    choice = 0
    print()
    for x in range(len(songs["docs"]) - 1):
        print(f"{x + 1}: {songs["docs"][x]["name"]} - Uploaded by {songs["docs"][x]["uploader"]["name"]}\n")
        lines += 2
    try:
        lines += 2
        choice = int(input("Enter corresponding number to choose song, anything else will return to menu: "))
    except KeyboardInterrupt:
        quit()
    except:
        returnNlinesUp(lines)
        return
    if(choice > len(songs["docs"]) or choice < 1):
        returnNlinesUp(lines)
        return
    url = songs["docs"][choice - 1]["versions"][0]["downloadURL"]
    filename = "_garbage.zip"
    folder = "Songs/"
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    with zipfile.ZipFile(filename) as zip_ref:
        try:
            info = json.load(zip_ref.open("info.dat"))
        except:
            info = json.load(zip_ref.open("Info.dat"))
        if info["_version"] != "2.0.0":
            print("beatmap not version 2.0.0")
            lines += 1
        folder += info['_songName']
        folder = folder.replace("'", "").replace("\"", "")
        zip_ref.extractall(folder)
    os.remove(filename)
    returnNlinesUp(lines)

def chooseGameType():
    print("Game types:")
    print("1: terminal")
    print("2: serial")
    print("3: pygame")
    lines = 4
    invalidChoice = True
    prompt = "Enter corresponding number to make a game selection: "
    while(invalidChoice):
        try:
            num = int(input(prompt))
        except KeyboardInterrupt:
            quit()
        except:
            returnNlinesUp(1)
            prompt = "Please enter a number: "
            continue
        if num < 1 or num > 3:
            returnNlinesUp(1)
            prompt = "Please enter a valid game choice: "
        else:
            invalidChoice = False
    returnNlinesUp(lines + 1)
    return num

def chooseSong():
    if not os.path.isdir("./Songs"):
        print("No song files found!")
        quit()
    print("Available Songs:")
    lines = 1
    songList = next(os.walk('./Songs'))[1]
    for index, song in enumerate(songList):
        print(f"{index + 1}: {song}")
        lines += 1
    invalidChoice = True
    prompt = "Enter corresponding number to make a song selection: "
    while(invalidChoice):
        try:
            num = int(input(prompt))
        except KeyboardInterrupt:
            quit()
        except:
            returnNlinesUp(1)
            prompt = "Please enter a number: "
            continue
        if(num < 1 or num > len(songList)):
            returnNlinesUp(1)
            prompt = "Invalid song choice. Please try again: "
        else:
            invalidChoice = False
    checkFolder(f"./Songs/{songList[num - 1]}")
    returnNlinesUp(lines + 1)
    return f"./Songs/{songList[num - 1]}"

def sortDifficulty(file):
    if("Easy" in file):
        return 0
    if("Normal" in file):
        return 1
    if("Hard" in file):
        return 2
    if("ExpertPlus" in file or "Expert+" in file):
        return 4
    if("Expert" in file):
        return 3
    
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
    lines = 0
    for index, difficulty in enumerate(difficultyList):
        print(f"{index + 1}: {difficulty}")
        lines += 1
    invalidChoice = True
    prompt = "Enter corresponding number to make a difficulty selection: "
    while(invalidChoice):
        try:
            num = int(input(prompt))
        except KeyboardInterrupt:
            quit()
        except:
            prompt = "Please enter a number: "
            returnNlinesUp(1)
            continue
        if (num < 1 or num > len(difficultyList)):
            prompt = "Invalid song choice. Please try again: "
            returnNlinesUp(1)
        else:
            invalidChoice = False
    returnNlinesUp(lines + 1)
    return f"{songFolder}/{difficultyFileList[num-1]}"

def choosePort():
    print("Available Ports:")
    lines = 1
    comports = listports.comports()
    for index, port in enumerate(comports):
        print(f"{index}: {port.name} - {port.manufacturer}")
        lines += 1
    try:
        lines += 1
        num = int(input("Enter corresponding number to make a port selection or leave blank for debug: "))
    except KeyboardInterrupt:
        quit()
    except:
        print("Port not specified, entering debug mode")
        lines += 1
        returnNlinesUp(lines)
        return None
    if num < 0 or num >= len(comports):
        print("Invalid port choice, entering debug mode")
        lines += 1
        returnNlinesUp(lines)
        return None
    returnNlinesUp(lines)
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
                shutil.rmtree(fileName[:fileName.rfind("/")])
                quit()
            return info["_beatsPerMinute"]
    except:
        print(f"Failed to parse {fileName}")
        shutil.rmtree(fileName[:fileName.rfind("/")])
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
    if port != None:
        print("calibrating controllers.", end='\r')
        time.sleep(5)
        print("calibrating controllers..", end= '\r')
        time.sleep(5)
        print("calibrating controllers...")
        time.sleep(5)
        port.write(bytes(gameType))
        
    score = 0;
    print(f"BPM: {bpm}")
    screen = ScreenState()
    noteIndex = 0
    leftNotes = []
    rightNotes = []
    running = False
    if gameType == gameTypes.terminal:
        print("\n" * 15)
    elif gameType == gameTypes.pygame:
        pygame.init()
        screenHeight = 720
        screenWidth = 720
        gameScreen = pygame.display.set_mode([screenWidth, screenHeight])
        bgColor = (53, 47, 47)
        gameColor = (0, 0, 0)
        gameScreen.fill(bgColor)
        pygame.draw.rect(gameScreen, gameColor, (100, 0, (screenWidth - 200), screenHeight))
        pygame.display.flip()
        arrList = pygame.sprite.Group()
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.music.load(songFile)
        pygame.mixer.music.play()
    startTime = time.time()
    for beat in range(int(notesList[len(notesList) - 1].getTime() + 18) * 4):
        # print screen to serial port or terminal
        if port != None:
            port.write(bytes(screen.getScreen() + '\f', "utf-8"))
        if gameType == gameTypes.terminal:
            print(f"\033[16F{screen.getDebug()}", end="")
        if gameType == gameTypes.pygame:
            running = True
            for arrow in arrList:
                arrow.updatePos()
                if (arrow.offScreen() == True):
                    arrList.remove(arrow)
            arrList.update()
            gameScreen.fill(bgColor)
            pygame.draw.rect(gameScreen, gameColor, (100, 0, (screenWidth - 200), screenHeight))
            arrList.draw(gameScreen)
            hitBoxL = pygame.draw.rect(gameScreen, bgColor, (179.5, 443.5, 161, 193), 2)
            hitBoxR = pygame.draw.rect(gameScreen, bgColor, (389.5, 443.5, 161, 193), 2)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        while((time.time() - startTime) * bpm/60 <= (beat-15.25)/4):
            continue
        if(noteIndex >= len(notesList) or noteIndex < 0):
            screen.pushTwoNotes(None, None, port)
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
            screen.pushTwoNotes(None, None, port)
        while(len(leftNotes) > 0 and len(rightNotes) > 0):
            screen.pushTwoNotes(leftNotes[0], rightNotes[0], port)
            leftNotes.pop(0)
            rightNotes.pop(0)
        while(len(leftNotes) > 0):
            screen.pushTwoNotes(leftNotes[0], None, port)
            leftNotes.pop(0)
        while(len(rightNotes) > 0):
            screen.pushTwoNotes(None, rightNotes[0], port)
            rightNotes.pop(0)
        if (gameType == gameTypes.pygame):
            if (screen.notesListLeft[0] != None):
                arrList.add(Arrow(screen.notesListLeft[0], gameScreen))
            if (screen.notesListRight[0] != None):
                arrList.add(Arrow(screen.notesListRight[0], gameScreen))
    pygame.quit()

def returnNlinesUp(n):
    #while(n >= 16):
    #    print(f"\033[15F", end="\r")
    #    n -= 15
    print(f"\033[{n}F\033[J", end="\r")

if __name__ == "__main__":
    main()
