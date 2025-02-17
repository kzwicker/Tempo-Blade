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