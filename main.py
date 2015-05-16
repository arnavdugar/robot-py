import sys
import code
import robot
import position
import insect
import display
import arduino
import serialize
import controller

# Connect to Arduino
print(">>> arduino.connect()")
arduino_board = arduino.connect()

# Load Robot Data
serialize.package = sys.modules[__name__]
r = serialize.load("model.txt")

# Draw Window
window = display.Display()


# Define Cleanup Method
def exit():
    arduino_board.close()
    sys.exit()

# Build Controller
controller.robot = r
controller.arduino_board = arduino_board
controller.window = window
controller.arduino = arduino
controller.serialize = serialize
controller.filename = "model.txt"
controller.exit = exit
controller.init()
controller.draw_robot()


# Start Interaction
code.interact(">>> robot = Robot()", local=controller.__dict__)
