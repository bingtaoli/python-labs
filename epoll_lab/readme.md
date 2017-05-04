## 简单例子

核心择席shadowsocks的网络模块。

这个简单的例子完成功能为：监听9000端口，接受请求；有连接就accept并且回应hello, world字符串。

## 网络编程中系统异常处理

在ss中，`recv`这个操作加异常判断处理，recv这种系统调用会报错是常事，所以必须针对不同的错误类型采取不同措施。这一点在各语言的处理都是类似的，有触类旁通的感觉。

```py
# _on_remote_read in tcprelay.py
data = None
try:
    data = self._remote_sock.recv(BUF_SIZE)

except (OSError, IOError) as e:
    # (bt) EAGAIN: try receive again in non-blocking programming
    # EWOULDBLOCK: Operation would block, just happen in non-blocking programming.
    # ETIMEDOUT: Connection timed out
    # EINTR: Interrupted function call
    if eventloop.errno_from_exception(e) in \
            (errno.ETIMEDOUT, errno.EAGAIN, errno.EWOULDBLOCK):
        return
    if not data:
    # (bt) no data then destroy? client close socket?
    self.destroy()
    return
```

注意看本人的注释，不同的信号有不同的原因。

