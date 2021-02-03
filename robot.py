import time
import serial

class Robot:
    def __init__(self, port):
        self.serial = serial.Serial(port, 115200)
        # Wake up Grbl firmware
        self.serial.write(b"\r\n\r\n")
        time.sleep(2)   # Wait for Grbl to initialize
        self.serial.flushInput()  # Flush startup text in serial input
        # Set speed
        self.send("G1 F30000")

    def send(self, command, pause=.2):
        message = str.encode(command + '\n')
        self.serial.write(message)
        time.sleep(pause)
        result = self.serial.read(self.serial.in_waiting)
        result = result.strip().decode('utf-8')
        if result != "ok":
            print(result)
        else:
            pass