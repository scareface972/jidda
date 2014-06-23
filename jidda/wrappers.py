from datetime import datetime
from socket import SHUT_RDWR, error

from gevent import getcurrent, sleep
from gevent.select import select
from jidda.mixins.events import EventContext
from msgpack import loads, dumps, UnpackException

class BadPayload(Exception): pass

class Request(object):
    def __init__(self, socket, addr):
        self.addr = addr
        self.socket = socket
        socket.setblocking(0)
        socket.settimeout(0.3)
        self.time = datetime.utcnow()
        self.rfile = self.socket.makefile('rb')
        self.disconnected = False

        self.greenlet = getcurrent()
        self.listeners = EventContext()

    def configure_socket(self, fn):
        fn(self.socket)
        return fn

    def begin_listening(self, interval=0, timeout=0.3):
        while not self.disconnected:
            reader, _, _ = select([self.socket], [], [], timeout)
            if reader:
                response, event = self.recv(needed_event=True)
                self.listeners.trigger(event, response)
                if interval:
                    sleep(interval)

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
        bits = self.rfile.readline()
        if not bits:
            if needed_event:
                return None, None
            return
        content_length = int(bits.strip())
        payload = self.rfile.read(content_length + 1)
        event = self.rfile.readline().strip()
        if event == ':none':
            event = None

        try:
            payload = loads(payload[:-1])
            if not needed_event:
                return payload
            return payload, event

        except (ValueError, UnpackException) as error:
            raise BadPayload(error)

    def emit(self, event, data):
        return self.send(data, event_namespace=event)

    def send(self, message, event_namespace=None):
        payload = dumps(message)
        if event_namespace is None:
            event_namespace = ":none"
        string = '{length}\n{payload}\n{namespace}\n'.format(length=len(payload),
                                                           payload=payload,
                                                           namespace=event_namespace)
        self.socket.sendall(string)


class Response(Request):
    pass
