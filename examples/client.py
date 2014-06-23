from traceback import format_exc
from jidda.client import Client
c = Client('localhost:6000')

@c.on('connect')
def respond_connect(res):
    print(res.recv())
    while True:
        datum = res.recv()
        if datum is None:
            break
        print(datum)
    return True

@c.on('error')
def error(exception):
    print(format_exc(exception))
    return True

if __name__ == "__main__":
    c.connect(connections=3)
    c.disconnect()
