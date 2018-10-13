import datetime
import RPi.GPIO as GPIO

class human_detect(object):
    #初始化
    def __init__(self):
        self.last_has_person = datetime.datetime.now()
        self.last_none_person = datetime.datetime.now()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23,GPIO.IN)

    @property
    def has_person(self):
        return GPIO.input(23)