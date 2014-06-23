from datetime import datetime
from socket import SHUT_RDWR, error
from msgpack import loads, dumps, UnpackException
from gevent import getcurrent

class BadPayload(Exception): pass

class Request(object):
    def __init__(self, socket, addr):
        self.addr = addr
        self.socket = socket
        self.time = datetime.utcnow()
        self.rfile = self.socket.makefile('rb')
        self.disconnected = False
        self.greenlet = getcurrent()

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

    def recv(self):
        bits = self.rfile.readline()
        if not bits:
            return
        content_length = int(bits.strip())
        payload = self.rfile.read(content_length + 1)
        try:
            payload = payload[:-1]
            return loads(payload)
        except (ValueError, UnpackException) as error:
            raise BadPayload(error)

    def send(self, message):
        payload = dumps(message)
        string = '{length}\n{payload}\n'.format(length=len(payload), payload=payload)
        self.socket.sendall(string)


class Response(Request):
    pass
