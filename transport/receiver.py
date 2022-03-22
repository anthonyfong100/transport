import socket
import json
import select
import sys
from transport.datagram import AckDatagram, MessageDatagram
from transport.configs import STARTING_SEQ_NUMBER


class Receiver:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 0))
        self.port = self.socket.getsockname()[1]
        self.log("Bound to port %d" % self.port)

        self.remote_host = None
        self.remote_port = None
        self.received_message_datagrams = {}
        self.current_seq_number = STARTING_SEQ_NUMBER

    def send(self, ack_datagram: AckDatagram):
        self.socket.sendto(json.dumps(ack_datagram.serialize()).encode(
            'utf-8'), (self.remote_host, self.remote_port))

    def log(self, message):
        sys.stderr.write(message + "\n")
        sys.stderr.flush()

    def is_duplicate_message(self, seq_num: int) -> bool:
        return seq_num in self.received_message_datagrams

    def _print_message_datagram_in_order(self) -> None:
        while self.current_seq_number in self.received_message_datagrams:
            curr_datagram: MessageDatagram = self.received_message_datagrams[
                self.current_seq_number]
            print(curr_datagram.data, end='', flush=True)
            self.current_seq_number += 1

    def wait_and_read_socket(self) -> MessageDatagram:
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
            return message_datagram

    def run(self):
        while True:
            message_datagram = self.wait_and_read_socket()
            self.log("Received data message %s" %
                     message_datagram.seq_number)

            ack_datagram: AckDatagram = AckDatagram(
                message_datagram.seq_number)

            if not self.is_duplicate_message(message_datagram.seq_number):
                self.received_message_datagrams[message_datagram.seq_number] = message_datagram

            # Always send back an ack
            self.log(
                f"Sending acknowledgement message {ack_datagram.seq_number}")
            self.send(ack_datagram)

            self._print_message_datagram_in_order()
