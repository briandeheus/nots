from pathlib import Path
from sqlalchemy import MetaData, create_engine

import os
import logging
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Connection:
    def __init__(self):
        db_path = os.path.join(Path.home(), ".nots")
        db_name = "nots.sqlite3"
        self._db_location = os.path.join(db_path, db_name)

        if not os.path.isdir(db_path):
            os.mkdir(db_path)

        if not os.path.isfile(self._db_location):
            logging.debug("Initalizing new database at %s", self._db_location)

        self.engine = create_engine(f"sqlite:///{self._db_location}")
        self.metadata = MetaData(bind=self.engine)

    def destroy_database(self):
        os.remove(self._db_location)
        self.__init__()

    def commit(self):
        self._connection.commit()

    def get(self):
        return self._connection

    def exec(self, query, params=None):
        con = self.get()
        cur = con.cursor()

        if not params:
            params = []

        logging.debug(
            "Executing query:\n----\n" "%s\n----\nwith params %s", query, params
        )
        return cur.execute(query, params)


connection = Connection()
