#!/usr/bin/env python
# encoding: utf-8

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
