import time
from transport.datagram import MessageDatagram


class RttEstimator:
    def __init__(self, starting_rto_seconds, starting_rtt_seconds, rtt_smoothing_factor, rto_rtt_multipler):
        self.smoothed_rto_seconds = starting_rto_seconds
        self.smoothed_rtt_seconds = starting_rtt_seconds
        self.rtt_smoothing_factor = rtt_smoothing_factor
        self.rto_rtt_multiplier = rto_rtt_multipler

    def compute_smoothed_rtt(self, send_time_sec: float, recv_ack_time_sec: float) -> float:
        curr_rtt = recv_ack_time_sec - send_time_sec
        return self.smoothed_rtt_seconds * \
            self.rtt_smoothing_factor + \
            ((1 - self.rtt_smoothing_factor) * curr_rtt)

    def add_new_rtt_entry(self, original_message_datagram: MessageDatagram) -> None:
        # compute smoothed_rtt_seconds and smoothed_rto_seconds
        self.smoothed_rtt_seconds = self.compute_smoothed_rtt(
            original_message_datagram.send_time, time.time())
        self.smoothed_rto_seconds = self.smoothed_rtt_seconds * self.rto_rtt_multiplier
