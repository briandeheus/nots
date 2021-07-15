from sqlalchemy import Table, Column, String, func, select, and_
from lib.database import connection
from lib.types import TYPES, TYPES_LIST, CASTING_TABLE
from lib.defaults import DEFAULTS
from lib.output import Output
from resources import Verb, custom
from resources.builtin import resource as builtin_resource
from alembic.migration import MigrationContext
from alembic.operations import Operations

import logging

TABLE_NAME = "__nots_field"
NAMES = ("field", "fields")


def add_field(table: Table, name: str, type: str, default: str, resource: str):
    column = Column(name, TYPES[type])

    ctx = MigrationContext.configure(connection.engine.connect())
    op = Operations(ctx)
    op.add_column(table.name, column)

    statement = RESOURCE.insert().values(
        name=name, type=type, default=default, resource=resource
    )
    connection.engine.execute(statement)
    return column


def field_exists(resource: str, name: str):
    return (
        connection.engine.execute(
            (
                select([func.count()])
                .select_from(RESOURCE)
                .where(and_(RESOURCE.c.resource == resource, RESOURCE.c.name == name))
            )
        ).scalar()
        > 0
    )


def get_field(resource: str, name: str):
    return connection.engine.execute(
        RESOURCE.select().where(
            and_(RESOURCE.c.resource == resource, RESOURCE.c.name == name)
        )
    ).one()


def get_fields(resource: str):
    return connection.engine.execute(
        RESOURCE.select().where(and_(RESOURCE.c.resource == resource))
    ).all()


class Create(Verb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument(name="resource", required=True)
        self.add_argument(name="name", required=True)
        self.add_argument(name="type", required=False)
        self.add_argument(name="default", required=False)

    def execute(self, resource, name, type, default, **options):

        if not builtin_resource.resource_exists(name=resource):
            logging.error("This resource does not exist.")
            return

        resource_def = builtin_resource.get_resource(name=resource)

        if field_exists(resource=resource_def.table_name, name=name):
            logging.error("This field already exist.")
            return

        if type and type not in TYPES:
            logging.error(
                "Invalid type %s. Choices are: %s", type, ", ".join(TYPES_LIST)
            )

        if not type:
            type = "text"

        logging.debug(
            "Creating field %s for resource %s, type is %s and default is %s",
            name,
            resource,
            type,
            default,
        )

        table = custom.create_table_def(name=resource)
        add_field(
            table=table,
            name=name,
            type=type,
            default=default,
            resource=resource_def.table_name,
        )

        if default:
            # make sure to get the new table definition
            if default in DEFAULTS:
                value = DEFAULTS[default]()
            else:
                value = CASTING_TABLE[type].cast_to(value=default)

            # We gotta fetch the column again.
            table = custom.create_table_def(name=resource)
            connection.engine.execute(table.update().values(**{name: value}))


class List(Verb):
    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)
        self.add_argument(name="resource", required=True)

    def execute(self, **options):
        output = Output(headers=["name", "type", "default", "resource"])
        resource = builtin_resource.get_resource(name=options["resource"])

        for field in get_fields(resource=resource.table_name):
            output.add_row(field)

        output.render_as_table()


VERBS = {"create": Create, "list": List}

RESOURCE = Table(
    TABLE_NAME,
    connection.metadata,
    Column("name", String),
    Column("type", String),
    Column("default", String),
    Column("resource", String),
)
