#!/usr/bin/env python
# encoding: utf-8


import threading
import time


class A:

	def __init__(self):
		self.shared_obj = {'hello': 'hello, world'}

	def run(self):
		i = 0
		while (i < 100):
			i += 1
			# exception happen during running
			if i == 5:
				raise Exception
			time.sleep(1)

	def close(self):
		print "shared_obj is closed"
		del self.shared_obj['hello']

class B:

	def __init__(self, a):
		self.shared_obj = a.shared_obj
		self.stop = False

	def run(self):
		i = 0
		while (i < 100 and self.stop is False):
			time.sleep(1) 
			print self.shared_obj['hello']
			i += 1

	def close(self):
		self.stop = True


def a_func():
	a.run()


def b_func():
	b.run()


if __name__ == '__main__':
	a = A()
	b = B(a)
	t1 = threading.Thread(target=b_func)
	try:
		t1.start()
		a.run()
	finally:
		b.close()
		t1.join()
		a.close()