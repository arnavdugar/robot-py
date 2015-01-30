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
arduino.connect()

# Load Robot Data
serialize.package = sys.modules[__name__]
r = serialize.load("model.txt")

# Draw Window
window = display.Display()

# Build Controller
controller.robot = r
controller.window = window
controller.arduino = arduino
controller.serialize = serialize
controller.filename = "model.txt"
controller.init()
controller.draw_robot()

# Start Interaction
code.interact(">>> robot = Robot()", local=controller.__dict__)