import subprocess
import serial

arduino = None


def list_devices():
    cmd = "ls /dev/tty.usbmodem* /dev/cu.usbmodem*"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data, err = process.communicate()
    if err:
        return
    return [line for line in data.decode("utf-8").split('\n') if line != '']


def select_device(data):
    print("0: None")
    for index in range(len(data)):
        print("%d: %s" % (index + 1, data[index]))
    while True:
        i = int(input("Select a USB port: "))
        if i is 0:
            return
        elif i > 0 and i <= len(data):
            break
        else:
            print("Invalid selection!")
    return data[i - 1]


def load_device():
    data = list_devices()
    if not data:
        print("Unable to find Arduino")
        return
    elif len(data) is not 1:
        return select_device(data)
    else:
        return data[0]


def connect(device=None, speed=115200):
    global arduino
    if not device:
        device = load_device()
    if not device:
        return
    arduino = serial.Serial(device, speed)


def write(value):
    global arduino
    if arduino:
        arduino.write(value)


def close():
    global arduino
    if arduino:
        arduino.close()