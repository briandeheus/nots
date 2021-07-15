from sqlalchemy import Table, Column, String, Integer
from lib.database import connection
from lib.output import Output
from resources import Verb
from sqlalchemy import select, insert, or_, func
import logging

TABLE_NAME = "__nots_resource"
NAMES = ("resource", "resources")


def get_resources():
    return connection.engine.execute(select(RESOURCE)).all()


def get_resource(name):
    return connection.engine.execute(
        select(RESOURCE).where(or_(RESOURCE.c.name == name, RESOURCE.c.plural == name))
    ).one()


def resource_exists(name):
    return (
        connection.engine.execute(
            (
                select([func.count()])
                .select_from(RESOURCE)
                .where(or_(RESOURCE.c.name == name, RESOURCE.c.plural == name))
            )
        ).scalar()
        > 0
    )


class Create(Verb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument(name="name", required=True)
        self.add_argument(name="plural", required=False)

    def execute(self, name, plural=None, **options):
        if not plural:
            plural = name

        if resource_exists(name):
            logging.error(
                "Resource with name %s or plurality %s already exists", name, plural
            )
            return

        connection.engine.execute(
            insert(RESOURCE).values(name=name, plural=plural, table_name=name)
        )

        table = Table(
            name,
            connection.metadata,
            Column("id", Integer(), autoincrement=True, primary_key=True),
        )
        table.create(bind=connection.engine)


class List(Verb):
    def execute(self, **options):
        output = Output(headers=["name", "plurality", "table"])
        for resource in get_resources():
            output.add_row(resource)

        output.render_as_table()


RESOURCE = Table(
    TABLE_NAME,
    connection.metadata,
    Column("name", String),
    Column("plural", String),
    Column("table_name", String),
)

VERBS = {"create": Create, "list": List}
