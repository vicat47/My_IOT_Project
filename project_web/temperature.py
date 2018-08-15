#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time, my_tools


'''
return data like this:
{
    "error_code" : error_code,
    "error_msg" : error_msg,
    "data" : {
        "temperature" : temperature,
        "humidity" : humidity,
        "check_data" : check,
        "sum_verification" : tmp
    }
}
'''
def get_current_temperature():

    sensor_data = get_sensor_data()

    while sensor_data.get('error_code') != 10000:
        time.sleep(5)
        sensor_data = get_sensor_data()
    
    return sensor_data

    

def get_sensor_data():

    channel =4

    data = []

    j = 0
    
    GPIO.setmode(GPIO.BCM)      #以BCM编码格式  
    
    time.sleep(1)           #时延一秒  

    GPIO.setup(channel, GPIO.OUT)  

    GPIO.output(channel, GPIO.LOW)
    
    time.sleep(0.02)        #给信号提示传感器开始工作  
    GPIO.output(channel, GPIO.HIGH)  

    GPIO.setup(channel, GPIO.IN)

    while GPIO.input(channel) == GPIO.LOW:  
        continue  
    
    while GPIO.input(channel) == GPIO.HIGH:  
        continue  
    
    while j < 40:  
        k = 0  
        while GPIO.input(channel) == GPIO.LOW:  
            continue  
        
        while GPIO.input(channel) == GPIO.HIGH:  
            k += 1  
            if k > 100:  
                break

        if k < 8:
            data.append(0)
        else:
            data.append(1)

        j += 1
    
    #重置针脚
    GPIO.cleanup()

    return data_change(data)

def data_change(data):
    humidity_bit = data[0:8]        #分组  
    humidity_point_bit = data[8:16]  
    temperature_bit = data[16:24]  
    temperature_point_bit = data[24:32]  
    check_bit = data[32:40]  
    
    humidity = 0  
    humidity_point = 0  
    temperature = 0  
    temperature_point = 0  
    check = 0  
    
    for i in range(8):  
        humidity += humidity_bit[i] * 2 ** (7 - i)              #转换成十进制数据  
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)  
        temperature += temperature_bit[i] * 2 ** (7 - i)  
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)  
        check += check_bit[i] * 2 ** (7 - i)  
    
    tmp = humidity + humidity_point + temperature + temperature_point       #十进制的数据相加  

    return_data = {
        "temperature" : temperature,
        "humidity" : humidity,
        "check_data" : check,
        "sum_verification" : tmp
    }
    
    if check == tmp:                                #数据校验，相等则输出  
        if temperature >= 50 or humidity > 100:
            return my_tools.get_error_message(10001, 'Not the right temperature', return_data)
        return my_tools.get_error_message(10000, 'Success to get temperature message...', return_data)
    else:                                       #错误输出错误信息，和校验数据
        return my_tools.get_error_message(10002, 'verification error, can not verification', return_data)

if __name__ == '__main__':
    get_current_temperature()