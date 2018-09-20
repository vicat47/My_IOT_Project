# 项目简介

![img](https://img.shields.io/badge/Language-Python-blue.svg) ![img](https://img.shields.io/badge/release-v0.1.0-green.svg)

该项目原本为本人假期闲来无事搞的一个iot项目，主要是使用树莓派控制家里空调。但是随着时间的推移，越来越多的功能加入了该项目。所以对本项目进行了重构，顺便加入了该README文档。

# 项目功能

该项目的主要功能目前有:
    - 通过串口发送消息，使用模块控制空调
    - 通过DHT11模块读写温度，写入温度数据库
    - 简陋的WEB端控制界面
    - 通过红外二极管发送红外数据

# 环境依赖

## 项目主要构成：
    - Python3
        - flask模块
    - SQLite
    - 树莓派
        - serial
        - GPIO
    - C
        - wirningPi

# 项目实现

## 项目实现方法

通过红外模块进行对空调的控制。该模块通过串口发送数据实现。

通过树莓派的串口对该模块进行控制。

其中温度传感器接在gpio7(pin7,BCM4),红外控制接在串口(pin8,pin10)

## 树莓派接线
|针脚|作用|
|:--:|:--:|
|1   |3.3v面包板供电|
|6   |面包板接地|
|7   |温度传感器DATA口|
|8   |TXD|
|10  |RXD|
|12  |pwm端口|
|13  |红外接收口|

## 数据库
|name|tdatetime|temperature(numeric)|humidity(integer)|
|:--:|:--:|:--:|:--:|
|RPi.CPU|now|1|0|

# 项目部署

```shell
git clone https://github.com/zsb514/My_IOT_Project.git
```

创建启动脚本
```
sudo vi /etc/init.d/服务名
```

脚本内容
```shell
#!/bin/bash
# /etc/init.d/mypyweb

### BEGIN INIT INFO
# Provides: embbnux
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: ledblink initscript
# Description: This service is used to manage a led
### END INIT INFO

case "$1" in
    start)
        echo "Starting WEB PROJECT"
        python3 /home/pi/你的项目路径/My_IOT_Project/project_web/app.py &
        ;;
    stop)
        echo "Stopping web project"
        #killall ledblink.py
        kill $(ps aux | grep -m 1 'python3 /home/pi/workspace/python/My_IOT_Project/project_web/app.py' | awk '{ print $2 }')
        ;;
    *)
        echo "Usage: service web project start|stop"
        exit 1
        ;;
esac
```

# 目录结构

待补充

# 待完成
- [ ] 页面优化
- [ ] 灯控制
- [ ] 接入人体传感器
- [ ] 面向对象重构项目
- [ ] 将配置保存为文件
- [ ] C接口的PWM控制

# 版本内容更新

## V0.1.0
- 一切的开始