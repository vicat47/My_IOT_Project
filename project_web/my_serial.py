import serial
import time
import string
import binascii

def open_serial():
    ser = serial.Serial('/dev/ttyAMA0', 9600)
    if ser.isOpen() == False:
        ser.open()
    return ser

def send_message(hex_data):
    s = open_serial()
    d = bytes.fromhex(hex_data)
    s.write(d)
    r = get_message(s)
    s.close()
    return 'success' + str(r)

def get_message(serial):
    s = serial
    n = s.inWaiting()
    if n:
        data = str(binascii.b2a_hex(s.read(n)))[2:-1]
        return data
    return 0