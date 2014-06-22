from socket import SHUT_RDWR, error
from msgpack import loads, dumps, UnpackException
from gevent import getcurrent

class BadPayload(Exception): pass

class Request(object):
    def __init__(self, socket, addr):
        self.addr = addr
        self.socket = socket
        self.rfile = self.socket.makefile('rb')
        self.disconnected = False
        self.greenlet = getcurrent()

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
        content_length = int(self.rfile.readline().strip())
        payload = self.rfile.read(content_length)
        try:
            return loads(payload)
        except (ValueError, UnpackException) as error:
            raise BadPayload(error)

    def send(self, message):
        payload = dumps(message)
        string = '{length}\n{payload}'.format(length=len(payload), payload=payload)
        self.socket.sendall(string)


class Response(Request):
    pass
