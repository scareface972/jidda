from random import choice
from traceback import format_exc
from jidda.client import Client
c = Client('localhost:6000')

@c.on('connect')
def respond_connect(res):
    counter = []
    method = choice(['cos','sin'])
    res.send({'need':method, 'times':10})

    print('\x1b[1mRequesting %s data:\x1b[0m' % (method))

    @res.listeners.on('cos')
    @res.listeners.on('sin')
    def respond_sin(data):
        counter.append(data)
        if len(counter) == 10:
            res.disconnect()
        return True

    res.begin_listening()
    for item in counter:
        print(item)
    return True

@c.on('error')
def error(exception):
    print(format_exc(exception))
    return True

if __name__ == "__main__":
    c.connect(connections=10, async=False)
    c.disconnect()
