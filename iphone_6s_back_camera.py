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
        self.robot.send("G1 X-50 Y70 Z-22", 1)

    # Open app
    def open_app(self):
        # Go to app icon
        print("  Go to app icon")
        self.robot.send("G1 X-29 Y31 Z-22", .75)

        # Launch app
        print("  Launch app")
        self.robot.send("G1 X-29 Y31 Z-31")
        self.start_timestamp = time.perf_counter()
        self.robot.send("G1 X-29 Y31 Z-22")

        # Move the arm out of the way just enough to find the image
        self.robot.send("G1 X-50 Y70 Z-22")

    # Close app
    def close_app(self):
        self.robot.send("G1 X-44 Y44 Z-22")
        self.robot.send("G1 X-44 Y44 Z-33")
        self.robot.send("G1 X-44 Y44 Z-22")

    # Quit app
    def quit_app(self):
        self.close_app()

        # Bring up view of all apps
        # (Double tap the home button)
        self.robot.send("G1 X-44 Y44 Z-22", .5)
        self.robot.send("G1 X-44 Y44 Z-33")
        self.robot.send("G1 X-44 Y44 Z-22")
        self.robot.send("G1 X-44 Y44 Z-33")
        self.robot.send("G1 X-44 Y44 Z-22")

        # Quit the app
        self.robot.send("G1 X-10 Y55 Z-15", .5)
        self.robot.send("G1 X-10 Y55 Z-29")
        self.robot.send("G1 X30 Y55 Z-29")
        self.robot.send("G1 X30 Y55 Z-22")

        # Return to home screen
        # (Tap home button)
        self.robot.send("G1 X-44 Y44 Z-22", .5)
        self.robot.send("G1 X-44 Y44 Z-33")
        self.robot.send("G1 X-44 Y44 Z-22")