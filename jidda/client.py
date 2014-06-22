from gevent import spawn, joinall
from gevent.socket import socket

from jidda.events import EventContext
from jidda.wrappers import Response
from jidda.utils import parse_addr, runner_factory, MiddlewareContext

class Client(object):
    def __init__(self, addr, connections=1):
        self.addr = parse_addr(addr)
        self.connections = connections
        self.greenlets = []

        MiddlewareContext().mixin(self)
        EventContext().mixin(self)

    @property
    def connection(self):
        sock = socket()
        sock.connect(self.addr)
        return sock

    @property
    def callback(self):
        return runner_factory(self, Response)

    def connect(self):
        self.greenlets = []
        callback = self.callback
        for _ in range(self.connections):
            greenlet = spawn(callback, self.connection, self.addr)
            self.greenlets.append(greenlet)

    def disconnect(self):
        joinall(self.greenlets)
