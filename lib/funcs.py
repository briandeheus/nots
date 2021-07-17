def limit(query, value, **kwargs):
    return query.limit(value)


def offset(query, value, **kwargs):
    return query.offset(value)


def order_by(query, value, columns):
    sort_columns = value.split(",")
    table_columns = {c.name: c for c in columns}

    for column in sort_columns:
        col_name = column.replace("-", "")
        if "-" in column:
            query = query.order_by(table_columns[col_name].desc())
        else:
            query = query.order_by(table_columns[col_name].asc())

    return query


FUNCTIONS = {"limit": limit, "offset": offset, "sort": order_by}

FUNCTIONS_LIST = FUNCTIONS.keys()
