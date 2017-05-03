# 多线程使用

## 多线程简单例子

见`hello_world.py`文件。

## condition

python的threading包自带了condition类，这个类提供`wait()`和`notify_all()`函数，很方便多个线程等待一个条件阻塞，条件满足继续执行的场景。

```python
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

"""
执行结果：
I am waiter_1, I am waiting
I am waiter_2, I am waiting
finally, you come, I am waiter 1
finally, you come, I am waiter 2
exit
"""
```

## 线程异常退出情况

本人在项目中使用多线程，主线程为A，开了两个线程B，C，共享A的log对象，在A异常退出时会清理log对象。所以遇到的问题就是A异常退出后，B和C没来得及退出还在用log对象，结果B和C也crash了。

还原场景，简化的代码如下：

```python
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
		t1.join()
	finally:
		b.close()
		a.close()
```

运行结果：

```
hello, world
hello, world
hello, world
shared_obj is closed
Traceback (most recent call last):
  File "share_one_obj.py", line 58, in <module>
    a.run()
  File "share_one_obj.py", line 20, in run
    raise Exception
Exception
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 801, in __bootstrap_inner
    self.run()
  File "/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 754, in run
    self.__target(*self.__args, **self.__kwargs)
  File "share_one_obj.py", line 49, in b_func
    b.run()
  File "share_one_obj.py", line 37, in run
    print self.shared_obj['hello']
KeyError: 'hello'
```

这个异常是在主线程a运行过程中手动触发的，程序会退出，也会影响b的线程，让b崩溃，按照合理的设计应该是b不要crash而是正常退出。

优化的改动很小，把`t1.join()`放在finally语句中，保证b退出后再销毁a的共享对象。

```python
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
```

运行结果和预期一致，不会影响b：

```
hello, world
hello, world
hello, world
hello, world
shared_obj is closed
Traceback (most recent call last):
  File "share_one_obj.py", line 58, in <module>
    a.run()
  File "share_one_obj.py", line 20, in run
    raise Exception
Exception
```

