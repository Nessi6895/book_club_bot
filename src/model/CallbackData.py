from enum import Enum
import json


class CallbackType(Enum):
    BOOK_VOTE = 1
    NOT_READING = 2


class CallbackData:

    def __init__(self, cb_type: CallbackType, data: 'dict[str, str]' = {}) -> None:
        self.cb_type = cb_type
        self.data = data

    def to_json(self) -> str:
        return json.dumps({'type': self.cb_type.name, 'data': self.data})


def parse_json(json_str: str) -> CallbackData:
    parsed = json.loads(json_str)
    cb_type = CallbackType[parsed["type"]]
    data = parsed["data"] if "data" in parsed else {}
    return CallbackData(cb_type, data)
