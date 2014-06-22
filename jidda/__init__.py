"""
    jidda
    ~~~~~

    Jidda makes creating socket-servers and highly
    scalable apps even simpler by providing a
    simple and robust communications framework.
    Usage examples::

        >>> from jidda.server import Server
        >>> app = Server('localhost:8000')
        >>> @app.on('connect')
        ... def connect(req):
        ...     req.send({'msg':'Hello World!'})
        ...     return True
        ...
        >>> app.run()

    Jidda builds on the shoulders of gevent and
    msgpack and simply allows you to write code
    with expressive syntactic sugar.
"""

from jidda.client import Client
from jidda.server import Server

VERSION = '0.0.3'
