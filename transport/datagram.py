from typing import Optional
import hashlib
import time


class MessageDatagram:
    def __init__(self, data: str, seq_number: int, checksum: Optional[str] = None):
        self.data: str = data
        self.seq_number: int = seq_number
        self.send_time: int = None
        self.checksum: str
        if checksum is None:
            self.checksum = self.hash()
        else:
            self.checksum = checksum

    def hash(self) -> str:
        hash_key = self.data + str(self.seq_number)
        return hashlib.md5(hash_key.encode()).hexdigest()

    def is_corrupted(self) -> bool:
        return self.hash() != self.checksum

    def serialize(self):
        return {
            "type": "msg",
            "data": self.data,
            "seq_number": self.seq_number,
            "checksum": self.checksum
        }

    @staticmethod
    def is_valid_serialized_message(payload: dict) -> bool:
        return "data" in payload and "seq_number" in payload and "checksum" in payload and payload["type"] == "msg"

    def is_timeout(self, rto_seconds: int) -> bool:
        return time.time() > self.send_time + rto_seconds


class AckDatagram:
    def __init__(self, seq_number: int, checksum: Optional[str] = None):
        self.seq_number: int = seq_number
        self.checksum: str
        if checksum is None:
            self.checksum = self.hash()
        else:
            self.checksum = checksum

    def hash(self) -> str:
        hash_key = str(self.seq_number)
        return hashlib.md5(hash_key.encode()).hexdigest()

    def is_corrupted(self) -> bool:
        return self.hash() != self.checksum

    def serialize(self):
        return {
            "type": "ack",
            "seq_number": self.seq_number,
            "checksum": self.checksum
        }

    @staticmethod
    def is_valid_serialized_message(payload: dict) -> bool:
        return "seq_number" in payload and "checksum" in payload and payload["type"] == "ack"
