import time,datetime
import entity.xiaomi_light,dao.human_detect
from threading import Thread

class human_sensor_control_light:
    def __init__(self, sensor, light):
        self.RUNNING = True
        self.xiaomi_light = light
        self.human_detect_sensor = sensor
        self.threading = Thread(target=self.detect_thread)

    def detect_thread(self):
        self.xiaomi_light.start()
        time.sleep(2)
        while self.RUNNING:
            now = datetime.datetime.now()
            if self.human_detect_sensor.has_person:
                if (now - self.human_detect_sensor.last_none_person).seconds > 120:
                    if self.xiaomi_light.status.get("power") is "off":
                        if (now - self.xiaomi_light.status.get("last_open")).seconds > 120:
                            self.xiaomi_light.send("power_on")
                self.human_detect_sensor.last_has_person = now
            else:
                if (now - self.human_detect_sensor.last_has_person).seconds > 120:
                    if self.xiaomi_light.status.get("power") is "on":
                        if (now - self.xiaomi_light.status.get("last_close")).seconds > 120:
                            self.xiaomi_light.send("power_off")
                self.human_detect_sensor.last_none_person = now
            time.sleep(6)
            
    def start(self):
        if self.threading.is_alive():
            return
        self.threading.start()

if __name__ == "__main__":
    h = human_sensor_control_light(entity.xiaomi_light.light(),dao.human_detect.human_detect())
    h.start()