from collections import defaultdict
from gevent import spawn, joinall
from gevent.socket import socket

from jidda.request import Response
from jidda.utils import parse_addr

class Client(object):
    def __init__(self, addr, connections=1):
        self.addr = parse_addr(addr)
        self.events = defaultdict(list)
        self.connections = connections
        self.greenlets = []

    def trigger(self, event, *args, **kwargs):
        for item in self.events[event]:
            if not item(*args, **kwargs):
                break

    def on(self, event):
        def wrapper(fn):
            self.events[event].append(fn)
            return fn
        return wrapper

    @property
    def connection(self):
        sock = socket()
        sock.connect(self.addr)
        return sock

    @property
    def callback(self):
        def function(socket):
            response = Response(socket, self.addr)
            print(response.recv())
            try:
                self.trigger('connect', response)
                self.trigger('disconnect', response)
            except Exception as error:
                self.trigger('error', error)
            finally:
                response.disconnect()
                self.trigger('teardown', response)
        return function

    def connect(self):
        self.greenlets = []
        callback = self.callback
        for _ in range(self.connections):
            greenlet = spawn(callback, self.connection)
            self.greenlets.append(greenlet)

    def disconnect(self):
        joinall(self.greenlets)
