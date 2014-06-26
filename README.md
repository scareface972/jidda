jidda
=====

Simple, fast, and scalable composable socket
servers based on `gevent` and `msgpack`. A very
simple example of a server:

```python
import time
from math import sin
from jidda.server import Server
app = Server('localhost:8000')

@app.on('connect')
def respond_connect(req):
    data = req.recv()
    for i in range(data.get('times', 10)):
        req.emit('sin', sin(time.time()))
    return True

if __name__ == "__main__":
    app.run(debug=True)
```

And the corresponding client code, that will
get the sin-ififed seconds since epoch and
print them:

```python
from jidda.client import Client
client = Client('localhost:8000')

@client.on('connect')
def connect(res):
    res.ctx.stack = []

    @res.listeners.on('sin')
    def enqueue_sin(data):
        res.ctx.stack.append(data)

    res.begin_listening()
    for item in res.ctx.stack:
        print(item)
    return True

if __name__ == "__main__":
    client.connect(connections=1)
    client.disconnect()
```

## Notes

Currently `jidda` only works for Python 2.x
because there appears to be some problems in
the gevent library for Python 3. There will
not be any dedicated ports to Python 3 since
I will not be actively using that platform
so if you are using Python 3 you will either
have to wait or (recommended) drop down to
Python 2 since most libraries are using Python
2 at the moment.
