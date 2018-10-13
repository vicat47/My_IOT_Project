from dao.human_detect import human_detect
from entity.xiaomi_light import light
from controller.light_control_thread import human_sensor_control_light

if __name__ == "__main__":
    h = human_detect()
    l = light()
    hl = human_sensor_control_light(h,l)
    hl.start()
