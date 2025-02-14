import json
import os

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


cwd = os.getcwd()
fileName = None
fileParsed = False

for root, dirs, files in os.walk(cwd):
    for name in files:
        if name.endswith((".dat")):
            fileName = os.path.join(cwd, name)
            print(fileName)

if fileName != None:
    with open(fileName) as data:
        parsedFile = json.load(data)
        print("parsed the file!")
        fileParsed = True
else:
    print("file not found!")

if fileParsed == True:
    notesList = []
    direction = 0

    for url in parsedFile["_notes"]:
        direction = url["_cutDirection"]
        if direction >= 4:
            direction = direction // 4
        notesList.append(Note(url["_time"], url["_type"], direction))
    data = open(cwd + "\\data.csv", "w")
    for notes in notesList:
        data.write(f"{notes.getTime()}, {notes.getColor()}, {notes.getDirection()}\n")
    data.close()

