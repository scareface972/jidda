from time import time
from math import sin, cos
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
    data = req.recv()
    method = sin if data['need'] == 'sin' else cos
    for item in range(data['times']):
        req.emit(data['need'], method(time()))
    return True

if __name__ == "__main__":
    server.run(debug=True)
