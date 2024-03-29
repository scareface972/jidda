from gevent import spawn, joinall
from gevent.socket import socket

from jidda.wrappers import Response
from jidda.utils import parse_addr, runner_factory
from jidda.mixins.events import EventContext
from jidda.mixins.middleware import MiddlewareContext

__all__ = ['Client']

class Client(object):
    def __init__(self, addr):
        self.addr = parse_addr(addr)
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

    def connect(self, connections=1, async=True):
        self.greenlets = []
        callback = self.callback
        for _ in range(connections):
            greenlet = spawn(callback, self.connection, self.addr)
            if not async:
                greenlet.join()
            self.greenlets.append(greenlet)

    def disconnect(self):
        joinall(self.greenlets)
        results = []
        for item in self.greenlets:
            results.append(item.value)
        return results
