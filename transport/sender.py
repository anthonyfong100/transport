import socket
import json
import select
import sys
from transport.configs import DATA_SIZE


class Sender:
    def __init__(self, host, port):
        self.host = host
        self.remote_port = int(port)
        self.log("Sender starting up using port %s" % self.remote_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 0))
        self.waiting = False

    def log(self, message):
        sys.stderr.write(message + "\n")
        sys.stderr.flush()

    def send(self, message):
        self.socket.sendto(json.dumps(message).encode(
            'utf-8'), (self.host, self.remote_port))

    def run(self):
        while True:
            sockets = [self.socket, sys.stdin] if not self.waiting else [
                self.socket]

            socks = select.select(sockets, [], [], 0.1)[0]
            for conn in socks:
                if conn == self.socket:
                    k, addr = conn.recvfrom(65535)
                    msg = k.decode('utf-8')

                    self.log("Received message '%s'" % msg)
                    self.waiting = False
                elif conn == sys.stdin:
                    data = sys.stdin.read(DATA_SIZE)
                    if len(data) == 0:
                        self.log("All done!")
                        sys.exit(0)

                    msg = {"type": "msg", "data": data}
                    self.log("Sending message '%s'" % msg)
                    self.send(msg)
                    self.waiting = True

        return
