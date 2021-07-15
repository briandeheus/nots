from lib.database import connection
from resources.builtin import field, resource
import logging

NAMES = ("system",)


def setup():
    logging.debug("Setting up nots.")
    connection.metadata.create_all(connection.engine)


def reset():
    logging.debug("Resetting nots to factory defaults.")
    connection.destroy_database()


VERBS = {"setup": setup, "reset": reset}
