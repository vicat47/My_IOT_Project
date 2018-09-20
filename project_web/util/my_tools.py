#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

def get_error_message(error_code, error_msg, data):
    res = {
        "error_code" : error_code,
        "error_msg" : error_msg,
        "data" : data
    }
    print(str(error_code) + ":" + error_msg + "    " + str(data))
    return res

def date_time_format(date_time):
    time = datetime.datetime.strftime(date_time,'%Y-%m-%d %H:%M:%S')
    return time