#!/usr/bin/env python
# encoding: utf-8

import time, threading

# 新线程执行的代码:
class HeadBeat():
    def __init__(self):
        self.stop = False

    def loop(self):
        print('thread %s is running...' % threading.current_thread().name)
        n = 0
        while n < 10 and self.stop is False:
            n = n + 1
            print('thread %s >>> %s' % (threading.current_thread().name, n))
            time.sleep(1)
        print('thread %s ended.' % threading.current_thread().name)

def loop(hb):
    hb.loop()

heart = HeadBeat()

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread', args=(heart,))
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)
