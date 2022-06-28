import socket

from Logs.log import Loggings

LOG = Loggings()
class usbServer:

    def __init__(self):
        HOST = "127.1.1.1"
        PORT = 1998
        self.ADDR = (HOST, PORT)
        self.sk_server = socket.socket()
        self.sk_server.bind(self.ADDR)
        self.sk_server.setblocking(False)
        self.sk_server.listen(5)

        LOG.info("建立usb连接", (HOST, PORT))
