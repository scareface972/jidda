from jidda.server import Server
server = Server('localhost:6000')

@server.on('connect')
def connect(req):
    req.send(['Hello World!'])

if __name__ == "__main__":
    server.run()
