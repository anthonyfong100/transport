class MessageDatagram:
    def __init__(self, data, seq_number):
        self.data = data
        self.seq_number = seq_number
        self.send_time = None

    def serialize(self):
        return {
            "type": "msg",
            "data": self.data,
            "seq_number": self.seq_number
        }


class AckDatagram:
    def __init__(self, seq_number):
        self.seq_number = seq_number

    def serialize(self):
        return {
            "type": "ack",
            "seq_number": self.seq_number
        }
