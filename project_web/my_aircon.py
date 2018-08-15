#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This class is the aircon class,be used controll the aircon and save aircon data.
'''

from my_serial import my_serial_controller

class aircon(object):

    def __init__(self):
        self.__last_open = None
        self.__last_close = None
        self.__is_open = False
        self.__serial_controller = my_serial_controller()

