from gevent import socket
from gevent.server import StreamServer

from jidda.mixins.events import EventContext
from jidda.mixins.middleware import MiddlewareContext
from jidda.utils import parse_addr, runner_factory, print_traceback_on_error
from jidda.wrappers import Request


class Server(object):
    def __init__(self, addr=None, timeout=2):
        self.addr = parse_addr(addr)
        self.timeout = timeout

        MiddlewareContext().mixin(self)
        EventContext().mixin(self)

    def setup_socket(self):
        if hasattr(self, 'socket'):
            return
        sock = socket.socket()
        sock.setblocking(0)
        sock.settimeout(self.timeout)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(self.addr)
        sock.listen(256)
        self.socket = sock

    def configure_socket(self, callback):
        self.setup_socket()
        callback(sock)
        return callback

    @property
    def callback(self):
        return runner_factory(self, Request, before=self.transform_request)

    def bind(self, addr):
        self.addr = parse_addr(addr)
        return self

    def run(self, **options):
        self.setup_socket()
        if 'debug' in options:
            debug = options.pop('debug')
            if debug:
                self.on('error')(print_traceback_on_error)

        server = StreamServer(self.socket, self.callback, **options)
        server.serve_forever()

