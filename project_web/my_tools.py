#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_error_message(error_code, error_msg, data):
    res = {
        "error_code" : error_code,
        "error_msg" : error_msg,
        "data" : data
    }
    print(error_msg + str(data))
    return res