from ctypes import *

class ir_sender(object):
    def __init__(self):
        self.c_ir_sender = CDLL('./sendIR.so')
        INPUT = c_int * 104
        self.c_array = INPUT()

    
    def send_waves(self, ir_code):
        self.set_send_code(ir_code)
        self.c_ir_sender.myPwnSender(self.c_array)
    
    def set_send_code(self, ir_code):
        for i in range(104):
            self.c_array[i] = ir_code[i]