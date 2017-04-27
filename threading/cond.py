#!/usr/bin/env python
# encoding: utf-8

import threading
import time

class Client:

    def __init__(self):
        self.cond = threading.Condition()
    
def trigger(client):
    time.sleep(10)
    with client.cond:
        client.cond.notify_all()

def waiter_1(client):
    with client.cond:
        print "I am waiter_1, I am waiting"
        client.cond.wait()
        print "finally, you come, I am waiter 1"

def waiter_2(client):
     with client.cond:
        print "I am waiter_2, I am waiting"
        client.cond.wait()
        print "finally, you come, I am waiter 2"

client = Client()
t1 = threading.Thread(target=trigger, name='trigger', args=(client,))
t2 = threading.Thread(target=waiter_1, name='waiter_1', args=(client,))
t3 = threading.Thread(target=waiter_2, name='waiter_2', args=(client,))
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()

print "exit"



