#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial, time, string, binascii, datetime, my_tools

class my_serial_controller(object):

    def __init__(self):
        self.__last_operate = None
        self.__can_operate = True
        self.__hex_mode = True

    def set_hex_mode(self, is_enabled):
        self.__hex_mode = is_enabled

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
        return my_tools.get_error_message(10000, 'Success to send serial message.',  str(r))

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


    def get_send_data(self, message):
        m = message
        if self.__hex_mode:
            m = bytes.fromhex(message)
        return m


    def do_serial_start(self, message):
        hex_data = self.get_send_data(message)
        time_now = self.verification(message)
        if not self.__can_operate:
            return my_tools.get_error_message(10012, "Can't operate the serial.Please wait...", hex_data)
        res = self.send_message(hex_data)
        if res.get('error_code') == 10000:
            self.__last_operate = time_now
        return res