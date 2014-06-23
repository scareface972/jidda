from msgpack import loads, dumps, UnpackException

__all__ = ['BadPayload','BadHeader','receive_message','send_message']

class BadPayload(ValueError): pass
class BadHeader(ValueError):  pass

def receive_message(stream):
    bits = stream.readline()
    if not bits:
        return

    if bits[0] != '#':
        raise BadHeader("Message doesn't start with '#'")

    bits = int(bits.strip()[1:])
    payload = stream.read(bits+1)[:-1]
    event = stream.readline().strip()
    try:
        return loads(payload), event
    except (ValueError, UnpackException) as exception:
        raise BadPayload(exception)

def send_message(socket, data, event):
    payload = dumps(data)
    if event is None:
        event = ':none'
    message = "#{bits}\n{payload}\n{event}\n".format(
            bits=len(payload),
            payload=payload,
            event=event
            )
    return socket.sendall(message)
