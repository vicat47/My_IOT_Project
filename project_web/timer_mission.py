#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from temperature import get_current_temperature
import datetime, time, threading, my_tools

def change_temp():
    res = get_current_temperature()
    temperature = res.get('data')
    temperature['time'] = my_tools.date_time_format(datetime.datetime.now())
    return temperature
    
'''
self.__sensor_data like this

{
    "time" : "2018-08-16 00:55:01"
    "temperature" : temperature,
    "humidity" : humidity,
    "check_data" : check,
    "sum_verification" : tmp
}
'''
class my_temperature_looper(object):
    def __init__(self):
        self.__is_running = True
        self.__thread = None
        self.__sensor_data = {}
        self.__aircon = []

    def set_aircon(self, data):
        self.__aircon = data
    
    def start_timer(self):
        self.__is_running = True
        while self.__is_running:
            self.__sensor_data = change_temp()
            for aircon in self.__aircon:
                aircon.ac_fixed_temperature(self.__sensor_data)
            time.sleep(120)
        
    def start_thread(self):
        if self.__thread == None:
            self.__thread = threading.Thread(target=self.start_timer, name='timer_thread')
        self.__thread.start()

    def get_sensor_data(self):
        return self.__sensor_data

    def stop(self):
        self.__is_running = False


if __name__ == '__main__':
    change_temp()