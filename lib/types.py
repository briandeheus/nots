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


class FloatParser:
    def cast_to(self, value):
        return float(value)


class IntParser:
    def cast_to(self, value):
        return int(value)


TYPES = {
    "datetime": DateTime,
    "text": String,
    "int": Integer,
    "float": Float,
    "boolean": Boolean,
}

CASTING_TABLE = {
    "boolean": Bool(),
    "text": Text(),
    "datetime": Datetime(),
    "int": IntParser(),
    "float": FloatParser(),
}

TYPES_LIST = TYPES.keys()
