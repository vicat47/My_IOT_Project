#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from entity.my_aircon import aircon
from dao.temperature import get_current_temperature
from controller.timer_mission import my_temperature_looper
from controller.light_control_thread import human_sensor_control_light
import dao.human_detect, entity.xiaomi_light
import threading, datetime

app = Flask(__name__)
my_temperature_changer = None
aircon_bedroom = aircon("bedroom")
light = entity.xiaomi_light.light()
human_detect = dao.human_detect.human_detect()
human_controller = human_sensor_control_light(human_detect, light)

'''
t like this
{
    "temperature" : 0,
    "humidity" : 0,
    "check_data" : 0,
    "sum_verification" : 0,
    "time" : "0:00",
    "is_open" : False,
    "last_open" : '0:00',
    "last_close" : '0:00',
    "is_fixed_temperature" : False
    "is_sleep_mode" : False
}
'''
@app.route('/', methods = ['GET', 'POST'])
def home():
    if my_temperature_changer:
        t = my_temperature_changer.get_sensor_data()
    aircon_data = aircon_bedroom.get_aircon_data
    t.update(aircon_data)
    return render_template("index.html", temperature=t)

@app.route('/open', methods = ['POST'])
def open():
    data = request.get_data().decode('utf-8')
    res = aircon_bedroom.ac_operate(data)
    return res.get("error_msg")

@app.route('/fixed_temperature', methods = ['POST'])
def fixed_temperture():
    return aircon_bedroom.set_fixed_temperature()

if __name__ == '__main__':
    aircon = [aircon_bedroom]
    my_temperature_changer = my_temperature_looper()
    my_temperature_changer.set_aircon(aircon)
    my_temperature_changer.start_thread()
    human_controller.start()
    # If want request from other hosts,shoud change param like this.
    app.run(host='0.0.0.0')
