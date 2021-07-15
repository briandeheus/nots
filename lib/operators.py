from lib.types import CASTING_TABLE


def eq(column, value):
    column_type = column.type.__visit_name__

    if column_type in CASTING_TABLE:
        return column == CASTING_TABLE[column_type].cast_to(value)

    return column == value


def neq(column, value):
    column_type = column.type.__visit_name__

    if column_type in CASTING_TABLE:
        return column != CASTING_TABLE[column_type].cast_to(value)

    return column != value


OPERATORS = {"eq": eq, "neq": neq, "gte": ""}
