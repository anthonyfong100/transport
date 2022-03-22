from tabnanny import check


class MessageDatagram:
    def __init__(self, data, seq_number, checksum=None):
        self.data = data
        self.seq_number = seq_number
        self.send_time = None
        if checksum is None:
            self.checksum = hash(self)
        else:
            self.checksum = checksum

    def __hash__(self) -> int:
        return hash(self.data + str(self.seq_number))

    def is_corrupted(self) -> bool:
        return hash(self) != self.checksum

    def serialize(self):
        return {
            "type": "msg",
            "data": self.data,
            "seq_number": self.seq_number,
            "checksum": self.checksum
        }


class AckDatagram:
    def __init__(self, seq_number, checksum=None):
        self.seq_number = seq_number
        if checksum is None:
            self.checksum = hash(self)
        else:
            self.checksum = checksum

    def __hash__(self) -> int:
        return hash(str(self.seq_number))

    def is_corrupted(self) -> bool:
        return hash(self) != self.checksum

    def serialize(self):
        return {
            "type": "ack",
            "seq_number": self.seq_number,
            "checksum": self.checksum
        }
