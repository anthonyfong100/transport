class CongestionWindowEstimator:
    def __init__(self, inital_window_size: int, slow_start_thresh_size: int) -> None:
        self._congestion_window_size: float = float(inital_window_size)
        self.slow_start_threshold: int = slow_start_thresh_size

    # modifies window size (straight from the slides)
    def receive_new_ack(self) -> None:
        if self._congestion_window_size < self.slow_start_threshold:
            # this is actually exponential
            self._congestion_window_size += 1
        else:
            # congestion avoidance, slow down
            self._congestion_window_size = self._congestion_window_size + \
                (1 / self._congestion_window_size)

    # modifies window size (straight from the slides)
    def receive_timeout(self) -> None:
        self.slow_start_threshold = self._congestion_window_size // 2
        self._congestion_window_size = 1

    def get_window_size(self) -> int:
        return int(self._congestion_window_size)
