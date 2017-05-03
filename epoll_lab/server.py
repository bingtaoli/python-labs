#!/usr/bin/env python
# encoding: utf-8


import eventloop
import socket
import logging

BUF_SIZE = 32 * 1024


class HelloWorld:

    def __init__(self):
        self.init_server_socket()
        # add to event loop
        loop = eventloop.EventLoop()
        self._eventloop = loop
        self._eventloop.add(self._server_socket, eventloop.POLL_IN | eventloop.POLL_ERR, self)
        self._fd_to_handlers = {}

    def run(self):
        print("listening...")
        self._eventloop.run()

    def init_server_socket(self):
        listen_address = '127.0.0.1'
        listen_port = 9000
        addrs = socket.getaddrinfo(listen_address, listen_port, 0, socket.SOCK_STREAM, socket.SOL_TCP)
        if len(addrs) == 0:
            raise Exception("can't get addrinfo for %s:%d" % (listen_addr, listen_port))
        af, socktype, proto, canonname, sa = addrs[0]
        server_socket = socket.socket(af, socktype, proto)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(sa)
        server_socket.setblocking(False)
        server_socket.listen(1024)
        self._server_socket = server_socket

    def handle_event(self, sock, fd, event):
        if sock:
            print 'handle fd %d %s' % (fd, eventloop.EVENT_NAMES.get(event, event))
        # (bt) new connection trigger server_socket
        if sock == self._server_socket:
            if event & eventloop.POLL_ERR:
                raise Exception('server_socket error')
            try:
                logging.debug('accept')
                conn = self._server_socket.accept()
                conn_sock = conn[0]
                conn_sock.setblocking(False)
                conn_sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
                # (bt) self is the handler
                loop = self._eventloop
                loop.add(conn_sock, eventloop.POLL_IN | eventloop.POLL_ERR, self)
            except (OSError, IOError) as e:
                error_no = eventloop.errno_from_exception(e)
                if error_no in (errno.EAGAIN, errno.EINPROGRESS,
                                errno.EWOULDBLOCK):
                    return
                else:
                    print ("%s" % str(e))
        else:
            if sock:
                data = None
                try:
                    data = sock.recv(BUF_SIZE)
                except (OSError, IOError) as e:
                    return
                if not data:
                    return
                print "reveived: %s" % data
                sock.send("hello, world")
                self.close_connection(sock)
            else:
                logging.warn('poll removed fd')

    def close_connection(self, conn_sock):
        self._eventloop.remove(conn_sock)
        print "close fd: %s" % conn_sock.fileno()
        conn_sock.close()

if __name__ == '__main__':
    h = HelloWorld()
    h.run()