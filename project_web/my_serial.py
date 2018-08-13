import serial, time, string, binascii, datetime

class my_serial_controller(object):

    def __init__(self):
        self.__last_open = None
        self.__last_close = None
        self.__is_open = False
        self.__last_operate = None
        self.__can_operate = True
        self.__send_switcher = {
            "SEND_IR_OPEN" : 'BB 01 FF',
            "SEND_IR_CLOSE" : 'BB 02 FF',
            "SEND_IR_SLEEP" : 'BB 03 FF',
            "LEARN_IR" : 'AA 01 FF'
        }

    def open_serial(self):
        ser = serial.Serial('/dev/ttyAMA0', 9600)
        if ser.isOpen() == False:
            ser.open()
        return ser

    def send_message(self, hex_data):
        s = self.open_serial()
        s.write(hex_data)
        r = self.get_message(s)
        s.close()
        return ['success', str(r)]

    def get_message(self, serial):
        s = serial
        n = s.inWaiting()
        if n:
            data = str(binascii.b2a_hex(s.read(n)))[2:-1]
            return data
        return 0

    def verification(self, message):
        time_now = datetime.datetime.now()

        if self.__last_operate != None:
            time_between_operate_seconds = (time_now - self.__last_operate).seconds
            if time_between_operate_seconds >= 5:
                self.__can_operate = True
            else:
                self.__can_operate = False
        return time_now


    def get_hex_data(self, message):
        d = self.__send_switcher.get(message, "none")
        if d != 'none':
            d = bytes.fromhex(d)
        return d


    def do_serial_start(self, message):
        hex_data = self.get_hex_data(message)
        if hex_data == "none":
            return 'No such data'
        time_now = self.verification(message)
        if not self.__can_operate:
            return "Can't operate.Please wait..."
        res = self.send_message(hex_data)
        if res[0] == 'success':
            if message == "SEND_IR_OPEN" or message == "SEND_IR_SLEEP":
                self.__last_open = time_now
                self.__is_open = True
            if message == "SEND_IR_CLOSE":
                self.__last_close = time_now
                self.__is_open = False
            self.__last_operate = time_now
        return res[0]