import ir_send

class ir_encoder(object):
    def __init__(self):
        self.ir_sender = ir_send.ir_sender()
        head = [1,1,0,0,0,0,1,1,1,1,1]
        other = []
        for i in range(72):
            if i == 21 or i == 30 or i == 37 or i == 61:
                other.append(1)
            else:
                other.append(0)
        self._code_format = {
            'head' : head,
            'temperature' : 16,
            'temperature_bin' : [0, 0, 0, 1, 0],
            'verification_bin' : [1, 0, 1, 0, 1],
            'other_bin' : other,
            'removal_verification_bin' : [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1]
        }

    def set_ir_data(self, temperature, open,is_open = False):
        self.data = {
            'last_tempture' : 26,
            'open' : open,
            'is_open' : is_open,
            'set_temperature' : temperature
        }

    def ir_encode(self, data):
        res = []
        res.extend(self._code_format.get('head'))
        temperature = self.data.get('temperature')

        last_tempture = self.data.get('last_temperature')
        if self.data.get('is_open') and temperature != last_tempture:
            if temperature > last_tempture:
                self._code_format['removal_verification_bin'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
            else:
                self._code_format['removal_verification_bin'] = [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
    
    def bin_add(arr, num):
        for i in range(num):
            arr += 1
            
                

    def is_need_carry(arr_of_num):
        for i in range(len(arr_of_num)):
            if arr_of_num[i] == 2:
                arr_of_num[i+1] += 1