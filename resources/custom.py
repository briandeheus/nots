from lib.database import connection
from lib.types import TYPES, CASTING_TABLE
from lib.defaults import DEFAULTS
from lib.operators import OPERATORS
from lib.output import Output
from lib.funcs import FUNCTIONS, FUNCTIONS_LIST
from lib import editor
from resources import Verb, ListVerb
from resources.builtin import resource as builtin_resource, field as builtin_field
from sqlalchemy import Table, Column, Integer, select

import logging


def create_table_def(name, columns=None):
    resource = builtin_resource.get_resource(name=name)
    table = Table(
        resource.table_name,
        connection.metadata,
        Column("id", Integer()),
        extend_existing=True,
    )

    for field in builtin_field.get_fields(resource=name):
        if columns and field.name not in columns:
            continue
        table.append_column(column=Column(field.name, TYPES.get(field.type)()))

    return table


def get_value(options, field):
    if options[field.name] is None:

        if field.default in DEFAULTS:
            value = DEFAULTS[field.default]()
        else:
            value = field.default

    elif options[field.name] == editor.ARG:
        value = editor.open_editor(field_name=field.name)

    else:

        value = options[field.name]

    return value


def build_execution_chain(query, table, options):
    for option in vars(options):

        if "__" not in option:
            logging.debug("Discarding %s for execution chain", option)

        column, op = option.split("__")

        if op not in FUNCTIONS_LIST:
            continue

        query = FUNCTIONS[op](
            query=query, value=getattr(options, option), columns=table.columns
        )

    return query


def build_query(table, options):
    all_columns = [c.name for c in table.columns]
    query = []

    for option in vars(options):

        if "__" not in option:
            logging.debug("Discarding %s for query", option)

        column, op = option.split("__")

        if op not in OPERATORS:
            continue

        if column not in all_columns:
            logging.error("Unknown field %s", column)
            exit(1)

        query.append(OPERATORS[op](getattr(table.c, column), getattr(options, option)))

    return query


class Delete(Verb):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_query(self, table):
        return build_query(table, self.unknown_options)

    def execute(self, **options):
        resource = builtin_resource.get_resource(name=options["resource"])
        table_def = create_table_def(name=resource.table_name)
        query = self.build_query(table=table_def)

        connection.engine.execute(table_def.delete().where(*query))


class Update(Verb):
    def __init__(self, argv, parent_args):
        super().__init__(argv, parent_args=parent_args)
        args = parent_args.parse_known_args(argv[1:])[0]

        self.resource = builtin_resource.get_resource(name=args.resource)
        self.fields = builtin_field.get_fields(resource=self.resource.table_name)
        self.field_map = {}

        for field in self.fields:
            self.field_map[field.name] = field
            self.add_argument(name=field.name, required=False)

    def execute(self, **options):
        values = {}

        table_def = create_table_def(name=self.resource.table_name)

        for field in self.fields:

            if field.name not in options:
                continue

            if options[field.name] is None:
                continue

            value = get_value(options, field)
            values[field.name] = CASTING_TABLE[field.type].cast_to(value)

        query = build_query(table=table_def, options=self.unknown_options)
        logging.debug(
            "Updating resource %s with values: %s", self.resource.table_name, values
        )
        connection.engine.execute(table_def.update(*query).values(**values))


class List(ListVerb):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_argument(name="fields", required=False)

    def build_query(self, table):
        return build_query(table, self.unknown_options)

    def execute(self, **options):

        if options.get("fields"):
            fields = options.get("fields").split(",")
        else:
            fields = None

        resource = builtin_resource.get_resource(name=options["resource"])
        table_def = create_table_def(name=resource.table_name)
        columns = []

        if fields:
            for f in fields:
                if hasattr(table_def.c, f):
                    columns.append(getattr(table_def.c, f))
        else:
            fields = [c.name for c in table_def.columns]
            columns = [c for c in table_def.columns]

        query = build_query(table=table_def, options=self.unknown_options)

        chain = build_execution_chain(
            query=select(*columns).where(*query),
            table=table_def,
            options=self.unknown_options,
        )

        output = Output(headers=fields)

        for row in connection.engine.execute(chain).all():
            output.add_row(row)

        output.render(mode=options["output"])


class Create(Verb):
    def __init__(self, argv, parent_args):
        super().__init__(argv=argv, parent_args=parent_args)
        args = parent_args.parse_known_args(argv[1:])[0]

        self.resource = builtin_resource.get_resource(name=args.resource)
        self.fields = builtin_field.get_fields(resource=self.resource.table_name)
        self.field_map = {}

        for field in self.fields:
            self.field_map[field.name] = field
            self.add_argument(name=field.name, required=field.default is None)

    def execute(self, **options):

        values = {}
        for field in self.fields:

            if field.name not in options:
                continue

            value = get_value(options, field)
            values[field.name] = CASTING_TABLE[field.type].cast_to(value)

        logging.debug(
            "Creating resource %s with values: %s", self.resource.table_name, values
        )
        table_def = create_table_def(name=self.resource.table_name)
        connection.engine.execute(table_def.insert().values(**values))


VERBS = {"create": Create, "list": List, "delete": Delete, "update": Update}
