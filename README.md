jidda
=====

Simple event-driven socket servers based on
`gevent` and `msgpack`. Usage example:

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
    client.connect()
    client.disconnect()
```

Currently it only works for Python 2.x because
there appears to be some problems in the gevent
library for Python 3.
