import inspect
import os
import time

class Phone:
    def __init__(self, robot=None):
        self.robot = robot
        self.clearance_height = "Z-22"
        self.tap_height = "Z-29"
        self.name = os.path.basename(inspect.getfile(Phone)).split('.')[0]

    # Go to starting position
    def go_to_start_position(self):
        self.robot.send("G1 X15 Y-100 Z0", 1)

    # Open app
    def open_app(self):
        # Go to app icon
        print("  Go to app icon")
        self.robot.send("G1 X15 Y-67 Z-22", .5)

        # Launch app
        print("  Launch app")
        self.robot.send("G1 X15 Y-67 " + self.clearance_height)
        self.robot.send("G1 X15 Y-67 " + self.tap_height)
        self.start_timestamp = time.perf_counter()
        self.robot.send("G1 X15 Y-67 " + self.clearance_height)

        # Move the arm out of the way just enough to find the image
        self.robot.send("G1 X0 Y-67 Z-22")

    # Close app
    def close_app(self):
        self.robot.send("G1 X0 Y-85 Z-15")
        self.robot.send("G1 X0 Y-85 Z-27")
        self.robot.send("G1 X0 Y-20 Z-27")
        self.robot.send("G1 X0 Y-20 Z-20")

    # Quit app
    def quit_app(self):
        # Bring up view of all apps
        self.robot.send("G1 F30000")
        self.robot.send("G1 X0 Y-85 Z-15")
        self.robot.send("G1 X0 Y-85 Z-27")
        self.robot.send("G1 X0 Y-30 Z-27")
        # This small pause makes sure the gesture isn't perceived as
        # "Close app and go to home screen".
        time.sleep(.20)
        self.robot.send("G1 X0 Y-30 Z-20")

        # Quit the app
        self.robot.send("G1 F30000")
        self.robot.send("G1 X25 Y-39 Z-15")
        self.robot.send("G1 X25 Y-39 Z-27")
        self.robot.send("G1 X25 Y20 Z-27")
        self.robot.send("G1 X25 Y20 Z-20")

        # Swip to return to home screen
        self.robot.send("G1 X0 Y-85 Z-15")
        self.robot.send("G1 X0 Y-85 Z-27")
        self.robot.send("G1 X0 Y-30 Z-27")
        self.robot.send("G1 X0 Y-30 Z-20")