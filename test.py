import json

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
    notesList = []
    try:
        with open("./Songs/RUSH E/ExpertPlus.dat") as notesFile:
            notesJSON = json.load(notesFile)
            if "_BPMChanges" in notesJSON and notesJSON["_BPMChanges"] != []:
                print("beatmap contains BPM changes")
                quit()
            direction = 0
            for note in notesJSON["_notes"]:
                direction = 8
                if "_cutDirection" in note:
                    direction = note["_cutDirection"]
                elif "_value" in note:
                    direction = note["_value"]
                notesList.append(Note(note["_time"], note["_type"], direction))
    except:
        print(f"Failed to parse")
        quit()
    for notes in notesList:
        print(notes.getTime())



main()


"""
import serial
import time

try:
    ser = serial.Serial('COM3', 9600)
    print("Serial port connected")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

try:
    while True:
        data_to_send = input("Enter data to send: ")
        ser.write(data_to_send.encode() + b'\n')
        time.sleep(1)
        
        if ser.in_waiting > 0:
            received_data = ser.readline().decode().strip()
            print(f"Received: {received_data}")

except KeyboardInterrupt:
    print("Exiting program")
finally:
    ser.close()
    print("Serial port closed")
"""