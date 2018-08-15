#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

def get_current_tempture():

    sensor_data = get_sensor_data()

    print("sensor is working.")
    print(sensor_data)             #输出初始数据高低电平
    while sensor_data == 'ERROR':
        time.sleep(5)
        print('error, try again')
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
    
    if check == tmp:                                #数据校验，相等则输出  
        print("temperature : " + str(temperature) + ", humidity : " + str(humidity))
        if temperature >= 50 or humidity > 100:
            return "ERROR"
        return [temperature, humidity]
    else:                                       #错误输出错误信息，和校验数据
        print("ERROR:" + "temperature : " + str(temperature) + ", humidity : " + str(humidity) + " check : " + str(check) + " tmp : " + str(tmp))
        return "ERROR"

if __name__ == '__main__':
    get_current_tempture()