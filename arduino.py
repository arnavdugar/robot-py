import serial
import struct
import subprocess
import threading
import time


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
        print("Unable to find Arduino.")
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
    arduino = Arduino(device)
    arduino.connect()
    return arduino


class Arduino:

    def __init__(self, device):
        self.device = device
        self.link = None
        self.listen_thread = None

    def connect(self, speed=115200, timeout=0):
        if self.link:
            if self.link.isOpen():
                print('Error Connecting: Device Already Connected')
                return
            try:
                self.link.open()
            except serial.SerialException:
                self.link.close()
                self.link.open()
        else:
            self.link = serial.Serial(self.device, speed, timeout=timeout)
        self.link.flushInput()
        if not (self.listen_thread and self.listen_thread.is_alive()):
            self.listen_thread = Listener(self.link)
            self.listen_thread.start()
            print('Starting Listener.')

    def isConnected(self):
        return self.link and self.link.isOpen()

    def write(self, data):
        self.link.write(data)
        self.link.flush()

    def close(self):
        self.link.close()

    def __exit__(self):
        self.link.close()


class Listener(threading.Thread):

    def __init__(self, arduino):
        threading.Thread.__init__(self)
        self.name = 'Listener'
        self.arduino = arduino

    def run(self):
        stream = b''
        while True:
            if not self.arduino.isOpen():
                print('\rTerminating Listener: Arudino Closed.\n>>> ', end='')
                return
            try:
                next = self.arduino.read()
            except:
                print('\rError Reading: Closing Connection.')
                self.arduino.close()
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
