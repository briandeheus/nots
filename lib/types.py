from sqlalchemy.types import String, Integer, Float, Boolean, DateTime
import dateparser


class Bool:
    def cast_to(self, value: str):
        return value.lower() == "true"


class Text:
    def cast_to(self, value):
        return str(value)


class Datetime:
    def cast_to(self, value):
        return dateparser.parse(value)


TYPES = {
    "datetime": DateTime,
    "text": String,
    "int": Integer,
    "float": Float,
    "boolean": Boolean,
}

CASTING_TABLE = {"boolean": Bool(), "text": Text(), "datetime": Datetime()}

TYPES_LIST = TYPES.keys()
