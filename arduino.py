import serial
import subprocess
import threading
import time

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
        try:
            i = int(input("Select a USB port: "))
        except ValueError:
            print("Invalid Input!")
            continue
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
    if not device and arduino:
        reconnect()
        return
    if not device:
        device = load_device()
    if not device:
        return
    arduino = serial.Serial(device, speed, timeout=0)
    initialize()


def reconnect():
    try:
        arduino.open()
    except serial.SerialException:
        arduino.close()
        arduino.open()
    initialize()


def initialize():
    global arduino
    arduino.flushInput()
    if not (hasattr(arduino, 'listen_thread') and arduino.listen_thread and arduino.listen_thread.is_alive()):
        arduino.listen_thread = Listener()
        arduino.listen_thread.start()
        print('Starting Listener.')



class Listener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.name = 'Listener'

    def run(self):
        global arduino
        stream = b''
        while True:
            if not arduino.isOpen():
                print('\rTerminating Listener: Arudino Closed.\n>>> ', end='')
                return
            try:
                next = arduino.read()
            except:
                print('\rError Reading: Closing Connection.')
                arduino.close()
                continue
            if len(next) == 0:
                time.sleep(0.2)
                continue
            start = 0
            for i in range(len(next)):
                if chr(next[i]) == '\n':
                    print('\r%s\n>>> ' % (stream + next[start:i]).decode("utf-8"), end='')
                    stream, start = b'', i + 1
            stream += next[start:]


def build_data(header, values):
    return struct.pack('!c%dH' % len(values), header, *values)


def write(data):
    global arduino
    if not arduino:
        return
    elif not arduino.isOpen():
        connect()
    else:
        arduino.write(data)
        arduino.flush()


def close():
    global arduino
    if not arduino:
        return
    else:
        arduino.close()
