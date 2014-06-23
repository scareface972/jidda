from msgpack import loads, dumps, UnpackException
class BadPayload(ValueError): pass

def recv(stream):
    bits = stream.readline()
    if not bits:
        return

    bits = int(bits.strip())
    payload = stream.read(bits+1)[:-1]
    event = stream.readline().strip()
    try:
        return loads(payload), event
    except (ValueError, UnpackException) as exception:
        raise BadPayload(exception)

def send(socket, data, event):
    payload = dumps(data)
    if event is None:
        event = ':none'
    message = "{bits}\n{payload}\n{event}\n".format(
            bits=len(payload),
            payload=payload,
            event=event
            )
    return socket.sendall(message)
