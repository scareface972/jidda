def parse_addr(string):
    if isinstance(string, tuple):
        return string
    addr, port = string.rsplit(':',1)
    return addr, int(port)
