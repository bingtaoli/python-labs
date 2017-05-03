一些日常使用python的记录

## 重试器

python的重试器，参见`retryer.py`，实现重试功能，灵感来自`kazoo`

## 多线程

多线程编程，参见`threading_labs`目录。包括condition使用、简单的多线程例子使用、一些遇需要注意的事项等。目录内单独有文档介绍。

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

## 日志类

基于python自带的logging包，使用handler实现按照天或者大小来分裂文件。代码摘自项目组前辈`magic`的封装，觉得挺实用的。见`logger.py`

## 处理日志[知乎笔试题]

阅读了一篇关于知乎笔试题的博客，地址如下：
`http://blog.csdn.net/liushuaikobe/article/details/9370587`，题目为处理日志。

看了一遍作者的代码，还是想按照自己的风格写，于是就按照自己的风格写了这道题目。见`log_parse_zhihu`目录。

## try finally

如果在except中加入return，finally会执行吗?

```python
def main():
    try:
        raise Exception
    except Exception as e:
        print "except: {}".format(str(e))
        return
    finally:
        print "finally"
    return
main()

"""
执行结果：
except:
finally
"""
```