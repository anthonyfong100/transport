import socket
import json
import select
import sys
from transport.datagram import AckDatagram, MessageDatagram


class Receiver:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 0))
        self.port = self.socket.getsockname()[1]
        self.log("Bound to port %d" % self.port)

        self.remote_host = None
        self.remote_port = None
        self.received_seq_numbers = set()

    def send(self, ack_datagram: AckDatagram):
        self.socket.sendto(json.dumps(ack_datagram.serialize()).encode(
            'utf-8'), (self.remote_host, self.remote_port))

    def log(self, message):
        sys.stderr.write(message + "\n")
        sys.stderr.flush()

    def is_duplicate_message(self, seq_num: int) -> bool:
        return seq_num in self.received_seq_numbers

    def run(self):
        while True:
            socks = select.select([self.socket], [], [])[0]
            for conn in socks:
                data, addr = conn.recvfrom(65535)

                # Grab the remote host/port if we don't alreadt have it
                if self.remote_host is None:
                    self.remote_host = addr[0]
                    self.remote_port = addr[1]

                msg = json.loads(data.decode('utf-8'))
                message_datagram: MessageDatagram = MessageDatagram(
                    msg["data"], int(msg["seq_number"]))
                self.log("Received data message %s" % message_datagram.data)

                if not self.is_duplicate_message(message_datagram.seq_number):
                    self.received_seq_numbers.add(message_datagram.seq_number)
                    print(message_datagram.data, end='', flush=True)

                    ack_datagram: AckDatagram = AckDatagram(
                        message_datagram.seq_number)

                    # Always send back an ack
                    self.send(ack_datagram)
