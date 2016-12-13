#!/usr/bin/env python
# encoding: utf-8

import time

def str_time_to_float(format_time):
    return time.mktime(time.strptime(str(format_time), "%Y-%m-%d %H:%M:%S"))

def unix_time_to_str(unix_time):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unix_time))

if __name__ == '__main__':
    print str_time_to_float("2016-12-13 20:00:00")
    print unix_time_to_str(time.time())
