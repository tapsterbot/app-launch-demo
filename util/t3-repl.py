# Path hack.
import sys, os
sys.path.insert(0, os.path.abspath('..'))

import time
import serial
from robot import Robot

# TODO: Make this a command line flag...
PORT = '/dev/ttyUSB0'

clearance_height = "Z-22"
tap_height = "Z-29"


robot = Robot(PORT)

def go(x = None,y = None, z = None):
    position = ""
    if x != None:
        position += " X" + str(x)
    if y != None:
        position += " Y" + str(y)
    if z != None:
        position += " Z" + str(z)
    print(position)
    robot.send("G1 " + position)

def tap(x = None,y = None):
    position = ""
    if x != None:
        position += " X" + str(x)
    if y != None:
        position += " Y" + str(y)
    print(position)
    robot.send("G1 " + position + " " + clearance_height)
    robot.send("G1 " + position + " " + tap_height)
    robot.send("G1 " + position + " " + clearance_height)

def double_tap(x = None,y = None):
    position = ""
    if x != None:
        position += " X" + str(x)
    if y != None:
        position += " Y" + str(y)
    print(position)
    robot.send("G1 " + position + " " + clearance_height)
    robot.send("G1 " + position + " " + tap_height)
    robot.send("G1 " + position + " " + clearance_height)
    robot.send("G1 " + position + " " + tap_height)
    robot.send("G1 " + position + " " + clearance_height)

#go(x=0, y=0, z=0)
go(0,0,0)