import json
from typing import Optional


def decode_bytes_to_json(msg: bytes) -> Optional[dict]:
    try:
        return json.loads(msg.decode('utf-8'))
    except:
        return None
