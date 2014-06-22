from collections import defaultdict
from socket import SOL_SOCKET, SO_REUSEADDR

from gevent import socket
from gevent.server import StreamServer

from jidda.utils import parse_addr
from jidda.request import Request

class Server(object):
    def __init__(self, addr, timeout=2):
        self.events = defaultdict(list)
        self.addr = parse_addr(addr)
        self.socket = socket.socket()
        self.timeout = timeout
        self.setup = False

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

    def on(self, event):
        def wrapper(fn):
            self.events[event].append(fn)
            return fn
        return wrapper

    def trigger(self, event, *args, **kwargs):
        for item in self.events[event]:
            if not item(*args, **kwargs):
                break

    def generate_runner(self):
        def handle_request(socket, address):
            request = Request(socket, address)
            try:
                self.trigger('connect', request)
                self.trigger('disconnect', request)
            except Exception as error:
                self.trigger('error', error)
            finally:
                request.disconnect()
                self.trigger('teardown', request)
        return handle_request

    def run(self, **options):
        self.setup_socket()
        server = StreamServer(self.socket, self.generate_runner(), **options)
        server.serve_forever()

