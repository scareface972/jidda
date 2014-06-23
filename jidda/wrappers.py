from datetime import datetime
from socket import SHUT_RDWR, error

from gevent import getcurrent, sleep, spawn
from gevent.select import select

from jidda.protocol import *
from jidda.mixins.events import EventContext
from msgpack import loads, dumps, UnpackException

class Request(object):
    def __init__(self, socket, addr):
        self.addr = addr
        self.socket = socket
        socket.setblocking(0)
        socket.settimeout(0.3)

        self.rfile = self.socket.makefile('rb')
        self.disconnected = False

        self.time = datetime.utcnow()
        self.ctx = type('_', (object,), {})

        self.greenlet = getcurrent()
        self.listeners = EventContext()

    def configure_socket(self, fn):
        fn(self.socket)
        return fn

    def begin_listening(self, interval=0, timeout=0.3, async=False):
        def callback():
            while not self.disconnected:
                reader, _, _ = select([self.socket], [], [], timeout)
                if reader:
                    response, event = self.recv(needed_event=True)
                    self.listeners.trigger(event, response)
                    if interval:
                        sleep(interval)
        if async:
            return spawn(callback)
        return callback()

    @property
    def peer(self):
        return ':'.join(map(str, self.addr))

    def disconnect(self):
        if self.disconnected:
            return
        try:
            self.socket.shutdown(SHUT_RDWR)
            self.socket.close()
        except error:
            pass
        finally:
            self.disconnected = True

    def recv(self, needed_event=False):
        response = receive_message(self.rfile)
        event = None
        if response:
            response, event = response

        if not needed_event:
            return response
        return response, event

    def emit(self, event, data):
        return self.send(data, event_namespace=event)

    def send(self, message, event_namespace=None):
        send_message(self.socket, message, event_namespace)

class Response(Request):
    pass
