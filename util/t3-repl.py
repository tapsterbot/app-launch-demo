import time
import serial

# TODO: Make this a command line flag...
PORT = '/dev/ttyUSB0'
CAPTURE_DEVICE = 2

clearance_height = "Z-22"
tap_height = "Z-29"

# Open serial port
robot = serial.Serial(PORT, 115200)

def init():
    # Wake up Grbl firmware
    robot.write(b"\r\n\r\n")
    time.sleep(2)   # Wait for Grbl to initialize
    robot.flushInput()  # Flush startup text in serial input
    # Set speed
    send("G1 F30000")

def send(command, pause=.2):
    message = str.encode(command + '\n')
    robot.write(message)
    time.sleep(pause)
    result = robot.read(robot.in_waiting)
    result = result.strip().decode('utf-8')
    if result != "ok":
        print(result)
    else:
        pass

def go(x = None,y = None, z = None):
    position = ""
    if x != None:
        position += " X" + str(x)
    if y != None:
        position += " Y" + str(y)
    if z != None:
        position += " Z" + str(z)
    print(position)
    send("G1 " + position)

def tap(x = None,y = None):
    position = ""
    if x != None:
        position += " X" + str(x)
    if y != None:
        position += " Y" + str(y)
    print(position)
    send("G1 " + position + " " + clearance_height)
    send("G1 " + position + " " + tap_height)
    send("G1 " + position + " " + clearance_height)

def double_tap(x = None,y = None):
    position = ""
    if x != None:
        position += " X" + str(x)
    if y != None:
        position += " Y" + str(y)
    print(position)
    send("G1 " + position + " " + clearance_height)
    send("G1 " + position + " " + tap_height)
    send("G1 " + position + " " + clearance_height)
    send("G1 " + position + " " + tap_height)
    send("G1 " + position + " " + clearance_height)

#go(x=0, y=0, z=0)
go(0,0,0)