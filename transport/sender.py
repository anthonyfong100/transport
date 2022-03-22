import socket
import json
import select
import sys
import time
from transport.configs import DATA_SIZE, STARTING_SEQ_NUMBER, DEFAULT_RTT_SECOND
from transport.datagram import MessageDatagram, AckDatagram
from typing import List

from transport.utils import decode_bytes_to_json


class Sender:
    def __init__(self, host, port, max_window_size):
        self.host = host
        self.remote_port = int(port)
        self.log("Sender starting up using port %s" % self.remote_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 0))
        self.max_window_size = max_window_size
        self.send_queue: List[MessageDatagram] = []
        self.send_buffer: List[MessageDatagram] = []
        self.seq_number = STARTING_SEQ_NUMBER
        self.should_terminate = False

    def log(self, message):
        sys.stderr.write(message + "\n")
        sys.stderr.flush()

    def _get_seq_number(self):
        seq_number = self.seq_number
        self.seq_number += 1
        return seq_number

    def send(self, msg_datagram: MessageDatagram):
        self.log(f"Sending data message {msg_datagram.serialize()}")
        msg_datagram.send_time = time.time()
        self.socket.sendto(json.dumps(msg_datagram.serialize()).encode(
            'utf-8'), (self.host, self.remote_port))

    def _remove_send_queue_by_seq_num(self, seq_num):
        self.send_queue = list(filter(lambda msg_datagram: msg_datagram.seq_number !=
                                      seq_num, self.send_queue))

    def should_terminate_sending(self):
        return self.should_terminate and len(self.send_buffer) == 0 and len(self.send_queue) == 0

    def read_from_input(self):
        socks = select.select([self.socket, sys.stdin], [], [], 0.1)[0]
        for conn in socks:
            if conn == self.socket:
                msg_bytes, _ = conn.recvfrom(65535)
                msg = decode_bytes_to_json(msg_bytes)
                if msg is not None and AckDatagram.is_valid_serialized_message(msg):
                    ack_datagram = AckDatagram(
                        int(msg["seq_number"]), msg["checksum"])
                    if not ack_datagram.is_corrupted():
                        self.log(
                            f"Received acknowledgement message {ack_datagram.seq_number}")
                        # remove message_datagram from send queue based on seq number
                        self._remove_send_queue_by_seq_num(
                            ack_datagram.seq_number)
                    else:
                        self.log(
                            f"Received corrupted acknowledgement message {ack_datagram.seq_number}")

            elif conn == sys.stdin:
                data = sys.stdin.read(DATA_SIZE)

                if len(data) == 0:
                    self.should_terminate = True
                    return  # no more data to be read terminate program

                datagram = MessageDatagram(data, self._get_seq_number())
                self.send_buffer.append(datagram)

    @staticmethod
    def _should_send_msg_datagram(msg_datagram: MessageDatagram):
        # send a datagram if not send before or if expires
        return msg_datagram.send_time is None or time.time() > msg_datagram.send_time + DEFAULT_RTT_SECOND

    def run(self):
        while True:
            self.read_from_input()

            if self.should_terminate_sending():
                self.log("All done!")
                sys.exit(0)

            # move item from buffer to send queue
            if (len(self.send_queue) < self.max_window_size) and self.send_buffer:
                self.send_queue.append(self.send_buffer.pop(0))

            # send message in buffer
            for msg_datagram in self.send_queue:
                if self._should_send_msg_datagram(msg_datagram):
                    self.send(msg_datagram)
