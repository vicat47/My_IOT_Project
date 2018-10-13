import socket,time, re, datetime
from threading import Thread

class light(object):
    def __init__(self):
        self.host = "192.168.8.142"
        self.port = 55443
        self.status = {
            "power" : "off",
            "bright" : "",
            "ct" : "",
            "color_mode" : "",
            "last_open" : "",
            "last_close" : ""
        }
        self.message = {
            "power_on" : b'{"id":1,"method":"set_power","params":["on", "smooth", 500]}\r\n',
            "power_off" : b'{"id":1,"method":"set_power","params":["off", "smooth", 500]}\r\n',
            "get_status" : b'{"id":1,"method":"get_prop","params":["power"]}\r\n',
            "toggle" : b'{"id":1,"method":"toggle","params":[]}\r\n'
        }
        self.listen_socket = None
        self.scan_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.message_squence = [0,0,0,0,0]
        self.message_squence_pointer = 0
        self.message_interval = Thread(target=self.message_detection_loop)
        self.RUNNING = True
    
    def send(self, send_message="get_status"):
        try:
            self.listen_socket.send(self.message.get(send_message))
        except Exception as e:
            print("Unexpected error:", e)

    def send_search_broadcast(self):
        '''
        multicast search request to all hosts in LAN, do not wait for response
        '''
        msg = "M-SEARCH * HTTP/1.1\r\n"
        msg = msg + "HOST: 239.255.255.250:1982\r\n"
        msg = msg + "MAN: \"ssdp:discover\"\r\n"
        msg = msg + "ST: wifi_bulb"
        self.scan_socket.sendto(msg.encode(), ('239.255.255.250', 1982))

    def message_detection_loop(self):
        search_interval = 30000
        read_interval = 100
        time_elapsed = 0

        if time_elapsed % search_interval == 0:
            self.send_search_broadcast()

        while self.RUNNING:
            was_scanned = False
            while not was_scanned:
                data = self.scan_socket.recv(2048)
                was_scanned = self.handle_search_response(data)
                if was_scanned:
                    break

            while True:
                self.handle_message_socket()
                data,address = self.listen_socket.recvfrom(2048)
                if data is not None:
                    self.message_squence[self.message_squence_pointer] = (eval(data.decode()))
                    self.update_status()
                    self.message_squence_pointer += 1
                    if self.message_squence_pointer == 5:
                        self.message_squence_pointer = 0
                        print(self.message_squence)
                print(self.status)
                time.sleep(read_interval/1000.0)
            time_elapsed += read_interval
            time.sleep(read_interval/1000.0)
        self.scan_socket.close()
        self.listen_socket.close()
        self.scan_socket, self.listen_socket = None, None

    def handle_message_socket(self):
        if self.listen_socket is None:
            self.listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.listen_socket.connect((self.host,self.port))
    
    def handle_search_response(self,data):
        '''
        Parse search response and extract all interested data.
        If new bulb is found, insert it into dictionary of managed bulbs. 
        '''
        data = data.decode("utf-8")
        location_re = re.compile(r"Location.*yeelight[^0-9]*([0-9]{1,3}(\.[0-9]{1,3}){3}):([0-9]*)")
        location_match = re.search(location_re, data)
        if location_match == None:
            return False
        self.host = location_match.group(1)
        self.port = int(location_match.group(3))
        
        self.status["power"] = self.get_param_value(data, "power")
        self.status["ct"] = self.get_param_value(data, "ct")
        self.status["bright"] = self.get_param_value(data, "bright")
        self.status["color_mode"] = self.get_param_value(data, "color_mode")
        self.status["last_open"] = datetime.datetime.now()
        self.status["last_close"] = datetime.datetime.now()
        
        print(self.status)

        self.scan_socket.close()
        self.scan_socket = None
        return True
    
    def start(self):
        if self.message_interval.is_alive():
            return
        self.message_interval.start()    

    def get_param_value(self, data, param):
        '''
        match line of 'param = value'
        '''
        param_re = re.compile(param + r":\s*([ -~]*)")  # match all printable characters
        match = param_re.search(data)
        value = ""
        if match != None:
            value = match.group(1)
            return value
        return None

    def update_status(self):
        params = self.message_squence[self.message_squence_pointer].get("params")
        bp = self.status["power"]
        if params is None:
            return
        for k in self.status.keys():
            r = params.get(k)
            if r is None:
                continue
            self.status[k] = r
        if bp != self.status["power"]:
            if self.status["power"] == "on":
                self.status["last_open"] = datetime.datetime.now()
            if self.status["power"] == "off":
                self.status["last_close"] = datetime.datetime.now()


if __name__ == "__main__":
    l = light()
    l.message_interval.start()
    time.sleep(2)
    l.send("toggle")
    l.message_interval.join()
