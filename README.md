jidda
=====

Simple, fast, and scalable composable socket
servers based on `gevent` and `msgpack`. A very
simple example of a server:

```python
from jidda.server import Server
app = Server('localhost:8000')

@app.on('connect')
def respond_connect(req):
    req.send({'msg':'Hello World!'})
    datum = req.recv()
    print(datum)
    return True

if __name__ == "__main__":
    app.run()
```

Middleware or request preprocessors can also
be used, and can be easily registered so they
can be ran programmatically when the request
is heard by the server:

```python
@app.use
def logger(req):
    string = '[{time}] {peer}'.format(time=req.time, peer=req.peer)
    print(string)
    return req
```

You can also preconfigure the server socket
to, for example, lower the timeout or tweak
some of the more advanced options using the
`configure_socket` decorator:

```python
@app.configure_socket
def config(socket):
    socket.settimeout(0.3)
```

And a simple client example that will take
the dictionary and invert it (make it's
keys it's values and vice-versa).

```python
from jidda.client import Client
client = Client('localhost:8000')

@client.on('connect')
def respond_connect(res):
    data = res.recv()
    res.send(dict((v,k) for k,v in data.items()))
    return True

if __name__ == "__main__":
    client.connect(connections=1)
    client.disconnect()
```

Currently `jidda` only works for Python 2.x
because there appears to be some problems in
the gevent library for Python 3. There will
not be any dedicated ports to Python 3 since
I will not be actively using that platform
so if you are using Python 3 you will either
have to wait or (recommended) drop down to
Python 2 since most libraries are using Python
2 at the moment.
