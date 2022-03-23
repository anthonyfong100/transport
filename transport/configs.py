DATA_SIZE = 1375
MAX_WINDOW_SIZE = 4
STARTING_SEQ_NUMBER = 0

# RTO_RTT_MULTIPLER is the multipler to determine retransmission time out (DEFAULT_RTO_SECOND) from round trip time (DEFAULT_RTT_SECOND)
# default RTT_SECOND (round trip time) assumed to be 0.5 seconds
# DEFAULT_RTO_SECOND (retransmission time out) defined to be RTO_RTT_MULTIPLER * DEFAULT_RTT_SECOND
RTO_RTT_MULTIPLER = 2
DEFAULT_RTT_SECOND = 0.5
DEFAULT_RTO_SECOND = DEFAULT_RTT_SECOND * RTO_RTT_MULTIPLER
# typically defined between 0.8 and 0.9 https://www.catchpoint.com/blog/tcp-rtt
RTT_SMOOTHING_FACTOR = 0.875
