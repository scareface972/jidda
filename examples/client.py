from jidda.client import Client
c = Client('localhost:6000')

@c.on('connect')
def respond_connect(res):
    print(res.recv())

if __name__ == "__main__":
    c.connect()
    c.disconnect()
