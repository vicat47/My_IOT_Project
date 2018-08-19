# IR的研究

该文件夹是对红外设备及红外协议进行研究的。

## 遥控器数据的获取

数据的获取由树莓派的红外接收配合LIRC进行接收，使用mode2 -d /dev/lirc0指令来生成原始的脉冲和静止数据。并手动(low的一匹)黏贴到ac_data文件中。。之后通过ir_read.py脚本写入data.txt中，再由Excel进行读取。。。

## 红外协议

我家的空调是aux的，可以从原始数据看出，是标准的NEC协议。该协议发送38KHz的脉冲，推荐的占空比是1/3.

该议初始发送9毫秒的脉冲，然后停止4.5毫秒。逻辑1为560微秒的脉冲+1.69毫秒的静止，逻辑0为560微秒的脉冲+560微秒的静息。

由此我首先想到的是BCM模块

## 树莓派的GPIO口
![gpio](http://imgsrc.baidu.com/forum/w%3D580/sign=525a7424f11f4134e0370576151e95c1/3be33ed7912397dd550071c35582b2b7d2a287dc.jpg)

## 发射红外

开始想的是使用python的gpio模块进行pwm操作，但是。。。由上，只能是。。  
为了做到微秒级别的时间控制，需要使用c语言进行编写发射模块。。。

### 安装wiringPi

### 通过GitHub安装
1. clone : git clone git://git.drogon.net/wiringPi
2. build : ./build
3. test : gpio -v, gpio readall

### wiringPi常用函数

[介绍](https://www.cnblogs.com/lulipro/p/5992172.html)

wiringPi的pwm函数有如下一条NOTE:

> Note: The PWM control functions can not be used when in Sys mode. To understand more about the PWM system, you’ll need to read the Broadcom ARM peripherals manual.

但是我不知道这里的系统模式是什么。。。待日后研究

要实现微秒级的控制，wiringPi提供了delayMicroseconds (unsigned int howLong)方法。

[wiringPi设置频率](http://tieba.baidu.com/p/4753142928)

[wiringPi官方树莓派特有函数](http://wiringpi.com/reference/raspberry-pi-specifics/)

## python 调用C 及 C++

1. 通过编译为DLL调用
2. 通过如下调用[python调用C/CPP](https://www.jianshu.com/p/cd28e8b0cce1)