#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This class is the aircon class,be used controll the aircon and save aircon data.
'''

from my_serial import my_serial_controller
import datetime, my_tools

class aircon(object):

    def __init__(self, position):
        self.position = position
        self.__last_open = None
        self.__last_close = None
        self.__is_open = False
        self.__is_fixed_temperature = False
        self.__is_sleep_mode = False
        self.__serial_controller = my_serial_controller()
        self.__aircon_switcher = {
            "SEND_IR_OPEN" : 'BB 01 FF',
            "SEND_IR_CLOSE" : 'BB 02 FF',
            "SEND_IR_SLEEP" : 'BB 03 FF'
        }

    def ac_operate(self, message):
        time_now = datetime.datetime.now()
        hex_data = self.__aircon_switcher.get(message, 'none')
        if hex_data == "none":
            return my_tools.get_error_message(10011, 'No such serial command.', hex_data)
        res = self.__serial_controller.do_serial_start(hex_data)
        if res.get('error_code') == 10000:
            if (not self.__is_open) and (message == "SEND_IR_OPEN" or message == "SEND_IR_SLEEP"):
                self.__last_open = time_now
                self.__is_open = True
                if message == "SEND_IR_SLEEP":
                    self.__is_sleep_mode = True
            elif self.__is_open and message == "SEND_IR_CLOSE":
                self.__last_close = time_now
                self.__is_open = False
                self.__is_sleep_mode = False
            return my_tools.get_error_message(10000, "Success to operate aircon", [])
        return res

    def ac_fixed_temperature(self, temperature):
        m = ''
        if self.__is_fixed_temperature:
            t = temperature.get('temperature')
            if t >= 29 and (not self.__is_open):
                self.ac_operate("SEND_IR_SLEEP")
                m = 'Up to fixed temperature 29 and operate ac make it sleep mode'
            elif t <= 26 and self.__is_open:
                self.ac_operate("SEND_IR_CLOSE")
                m = 'Down to fixed temperature 26 and operate ac make it close'
            return my_tools.get_error_message(10000, m, {})

    def set_fixed_temperature(self):
        self.__is_fixed_temperature = not self.__is_fixed_temperature
        if self.__is_fixed_temperature:
            return 'success to enable fixed temperature'
        return 'success to disable fixed temperature'

    def get_aircon_data(self):
        data = {
            "is_open" : self.__is_open,
            "last_open" : self.__last_open,
            "last_close" : self.__last_close,
            "is_fixed_temperature" : self.__is_fixed_temperature,
            "is_sleep_mode" : self.__is_sleep_mode
        }
        return data