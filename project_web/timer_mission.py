from tempture import get_current_tempture
import datetime, time, threading

def change_temp():
    f = open('/home/pi/workspace/python/project_web/static/js/data/tempture.js', 'w')
    tempture = get_current_tempture()
    time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    f.write("var current_tempture = ['" + str(tempture[0]) + "','" + str(tempture[1]) + "','" + time + "']")
    return tempture
    

class my_tempture_looper(object):
    def __init__(self):
        self.__is_running = True
        self.__thread = None
        self.__sensor_data = []
    
    def start_timer(self):
        while self.__is_running:
            self.__sensor_data = change_temp()
            time.sleep(120)
        
    def start_thread(self):
        if self.__thread == None:
            self.__thread = threading.Thread(target=self.start_timer, name='timer_thread')
        self.__thread.start()





if __name__ == '__main__':
    change_temp()