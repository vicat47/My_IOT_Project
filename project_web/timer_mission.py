from tempture import get_current_tempture
import datetime
import threading

def change_temp():
    f = open('/home/pi/workspace/python/project_web/static/js/data/tempture.js', 'w')
    tempture = get_current_tempture()
    time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    f.write("var current_tempture = ['" + str(tempture[0]) + "','" + str(tempture[1]) + "','" + time + "']")

def start_timer():
    change_temp()
    change_t = loop_timer(300, change_temp)
    change_t.run()
    return change_t

class loop_timer(threading.Timer):
    def __init__(self, interval, function, args=[], kwargs={}):
        threading.Timer.__init__(self, interval, function, args, kwargs)
    
    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                self.finished.set()
                break
            self.function(*self.args, **self.kwargs)

if __name__ == '__main__':
    change_temp()