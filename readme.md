一些日常使用python的记录

## 重试器

python的重试器，参见retryer.py：实现重试功能，steal from kazoo

## 多线程

多线程编程，参见threading_labs目录: 包括condition使用、helloworld级别多线程使用

## 网络请求

python使用urllib2发起网络请求

```py
request_data = "?area=81&encoding=false"
# use post method
urllib2.urlopen(urllib2.Request(url, request_data), timeout=10)
# use get method
urllib2.urlopen(urllib2.Request('%s%s' % (url, request_data)), timeout=10)
```

## 时间工具函数

一些自己使用的时间函数，参见time_utils.py

未完待续 :-)