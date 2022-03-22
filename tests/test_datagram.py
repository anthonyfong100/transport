import unittest
import hashlib
from transport.datagram import AckDatagram, MessageDatagram


class TestMessageDatagram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_data = "Testing message for datagram"
        cls.message_datagram = MessageDatagram(cls.sample_data, 0)

    def test_serialize(self):
        self.assertEqual(self.message_datagram.serialize(), {
            "type": "msg",
            "data": self.message_datagram.data,
            "seq_number": 0,
            "checksum": self.message_datagram.hash()
        })

    def test_is_corrupted(self):
        # message that sender sent
        original_message_datagram = MessageDatagram("original message", 0)

        # message that the receiver received
        corrupted_data_message_datagram = MessageDatagram(
            "message got coorrupted", 0, original_message_datagram.checksum)
        corrupted_seq_number_message_datagram = MessageDatagram(
            "original message", -1, original_message_datagram.checksum)

        uncorrupted_message_datagram = MessageDatagram(
            "original message", 0, original_message_datagram.checksum)

        self.assertTrue(corrupted_data_message_datagram.is_corrupted(
        ), "is_corrupted should equate to true since message got corrupted")
        self.assertTrue(corrupted_seq_number_message_datagram.is_corrupted(
        ), "is_corrupted should equate to true since seq_number got corrupted")

        self.assertFalse(uncorrupted_message_datagram.is_corrupted(
        ), "is_corrupted is false since data is successfully sent")

    def test_hash(self):
        hash_key = self.message_datagram.data + \
            str(self.message_datagram.seq_number)
        hash_val = hashlib.md5(hash_key.encode()).hexdigest()
        self.assertEqual(self.message_datagram.hash(), hash_val)


class TestAckDatagram(unittest.TestCase):
    @ classmethod
    def setUpClass(cls):
        cls.ack_datagram = AckDatagram(0)

    def test_serialize(self):
        self.assertEqual(self.ack_datagram.serialize(), {
            "type": "ack",
            "seq_number": 0,
            "checksum": hashlib.md5(str(self.ack_datagram.seq_number).encode()).hexdigest()
        })

    def test_is_corrupted(self):
        # message that sender sent
        original_ack_datagram = AckDatagram(0)

        # message that the receiver received
        corrupted_ack_datagram = AckDatagram(
            10, original_ack_datagram.checksum)

        uncorrupted_ack_datagram = AckDatagram(
            0, original_ack_datagram.checksum)

        self.assertTrue(corrupted_ack_datagram.is_corrupted(
        ), "is_corrupted should equate to true since seq_number got corrupted")

        self.assertFalse(uncorrupted_ack_datagram.is_corrupted(
        ), "is_corrupted is false since ack message is successfully sent")


if __name__ == '__main__':
    unittest.main()
