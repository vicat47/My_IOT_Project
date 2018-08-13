from flask import Flask, request, render_template
from my_serial import my_serial_controller
from tempture import get_current_tempture
from timer_mission import my_tempture_looper
import threading, datetime

app = Flask(__name__)
my_tempture_changer = None
serial_controller = my_serial_controller()

@app.route('/', methods = ['GET', 'POST'])
def home():
    t = [0, 0, 0]
    if my_tempture_changer != None and my_tempture_changer.get_sensor_data() != []:
        t = my_tempture_changer.get_sensor_data()
    return render_template("index.html", tempture=t)

@app.route('/open', methods = ['POST'])
def open():
    data = request.get_data().decode('utf-8')
    res = serial_controller.do_serial_start(data)
    return res

if __name__ == '__main__':
    my_tempture_changer = my_tempture_looper()
    my_tempture_changer.start_thread()
    # If want request from other hosts,shoud change param like this.
    app.run(host='0.0.0.0')
