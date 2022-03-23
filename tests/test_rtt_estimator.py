import unittest
import unittest.mock
from transport.datagram import MessageDatagram
from transport.rtt_estimator import RttEstimator
from transport.configs import DEFAULT_RTO_SECOND, DEFAULT_RTT_SECOND, RTO_RTT_MULTIPLER, RTT_SMOOTHING_FACTOR


class TestRttEstimator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rtt_estimator = RttEstimator(
            DEFAULT_RTO_SECOND, DEFAULT_RTT_SECOND, RTT_SMOOTHING_FACTOR, RTO_RTT_MULTIPLER)

    def test_compute_smoothed_rtt(self):
        start_time_seconds = 1000
        end_time_seconds = 1002
        expected_rtt = 0.875 * 0.5 + \
            (1-0.875) * (end_time_seconds - start_time_seconds)
        self.assertAlmostEqual(self.rtt_estimator.compute_smoothed_rtt(
            start_time_seconds, end_time_seconds), expected_rtt)

    # TODO: Mock the time.time for UT
    # # mock the send time for consistency in unit tests
    # @unittest.mock.patch('time.time')
    # def test_add_new_rtt_entry(self):
    #     rtt_estimator = RttEstimator(
    #         DEFAULT_RTO_SECOND, DEFAULT_RTT_SECOND, RTT_SMOOTHING_FACTOR, RTO_RTT_MULTIPLER)
    #     mock_message_datagram: MessageDatagram = MessageDatagram(
    #         "sample data message", 0)
    #     rtt_estimator.add_new_rtt_entry(mock_message_datagram)

    #     expected_rtt = 0.875 * 0.5 + \
    #         (1-0.875) * (1002 - 1000)
    #     expected_rto = expected_rtt * 10
    #     self.assertAlmostEqual(
    #         rtt_estimator.smoothed_rtt_seconds, expected_rtt)
    #     self.assertAlmostEqual(
    #         rtt_estimator.smoothed_rto_seconds, expected_rto)


if __name__ == '__main__':
    unittest.main()
