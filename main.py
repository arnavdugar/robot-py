import sys
import code
import robot
import position
import display
import arduino
import serialize

# Connect to Arduino
print(">>> arduino.connect()")
arduino.connect()

# Load Robot Data
r = serialize.load(sys.modules[__name__], "model.txt")

# Draw Window
window = display.Display()

# Build Context
context = {'robot': r, 'arduino': arduino, 'serialize': serialize}

context['l0'] = r.legs[0]
context['s0'] = r.legs[0].segments[0]

# Start Interaction

code.interact(">>> robot = Robot()", local=context)