from collections import defaultdict
from socket import SOL_SOCKET, SO_REUSEADDR

from gevent import socket
from gevent.server import StreamServer

from jidda.events import EventContext
from jidda.utils import parse_addr, runner_factory
from jidda.request import Request

class Server(object):
    def __init__(self, addr, timeout=2):
        self.addr = parse_addr(addr)
        self.socket = socket.socket()
        self.timeout = timeout
        self.setup = False

        self.middleware = []
        self.events = EventContext()
        self.events.mixin(self)

    def transform_request(self, request):
        for item in self.middleware:
            request = item(request)
        return request

    def use(self, fn):
        self.middleware.append(fn)
        return fn

    def setup_socket(self):
        if self.setup:
            return
        self.socket.setblocking(0)
        self.socket.settimeout(self.timeout)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.addr)
        self.socket.listen(256)
        self.setup = True

    def configure_socket(callback):
        callback(self.socket)
        return callback

    @property
    def callback(self):
        return runner_factory(self, Request, before=self.transform_request)

    def run(self, **options):
        self.setup_socket()
        server = StreamServer(self.socket, self.callback, **options)
        server.serve_forever()

