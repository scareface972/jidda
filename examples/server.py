from time import time
from math import sin
from traceback import format_exc
from jidda.server import Server
server = Server('localhost:6000')

@server.use
def logger(request):
    string = '[%s] - %s' % (request.time, request.peer)
    print(string)
    return request

@server.on('connect')
def connect(req):
    req.send(['Hello World!'])
    for item in range(10):
        req.emit('sin', sin(time()))
    return True

if __name__ == "__main__":
    server.run(debug=True)
