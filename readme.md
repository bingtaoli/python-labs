一些日常使用python的记录

## 重试器

python的重试器

```py
#!/usr/bin/env python
# encoding: utf-8
import time

"""
定义一个retry重试器, steal from kazoo
"""


class ForceRetryError(Exception):
    """
    just a name
    """


class ForceFailedError(Exception):
    """
    just a name
    """


class Retry(object):

    def __init__(self, max_tries=1, max_jitter=0.8, sleep_func=time.sleep):
        self.sleep_func = sleep_func
        self.max_jitter = max_jitter
        self.max_tries = max_tries
        self._attempts = 0

    def __call__(self, func, *args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except ForceRetryError:
                if self._attempts == self.max_tries:
                    raise ForceFailedError
                self._attempts += 1
            self.sleep_func(0.1)

def my_sleep_func(s):
    print "I am sleeping"
    time.sleep(s)


def retry_func():
    print "try again"
    global loop_times
    loop_times += 1
    if loop_times == 10:
        print "I am going to finish myself"
        return
    else:
        raise ForceRetryError
    

if __name__ == '__main__':
    loop_times = 0
    retry = Retry(max_tries=20, sleep_func=my_sleep_func)
    retry(retry_func)

```

## 多线程

多线程编程

```py
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
```

## 网络请求

python使用urllib2发起网络请求

```py
request_data = "?area=81&encoding=false"
# use post method
urllib2.urlopen(urllib2.Request(url, request_data), timeout=10)
# use get method
urllib2.urlopen(urllib2.Request('%s%s' % (url, request_data)), timeout=10)
```

### wait and see
