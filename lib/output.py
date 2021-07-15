from beautifultable import BeautifulTable

import json
import logging


class Output:
    def __init__(self, headers):
        self.headers = headers
        self.rows = []

        self.RENDER_MODES = {"table": self.render_as_table, "json": self.render_as_json}

        self.RENDER_MODES_LIST = self.RENDER_MODES.keys()

    def render(self, mode):
        if mode not in self.RENDER_MODES:
            logging.error(
                "Mode %s not in render modes. Valid choices: %s",
                mode,
                ", ".join(self.RENDER_MODES_LIST),
            )

        self.RENDER_MODES[mode]()

    def add_row(self, row):
        self.rows.append(row)

    def render_as_json(self):
        rows = []
        for row in self.rows:
            rows.append({key: row[key] for key in row.keys()})
        print(json.dumps(rows, indent=2))

    def render_as_table(self):
        table = BeautifulTable()
        table.set_style(BeautifulTable.STYLE_NONE)
        table.columns.header = [h.upper() for h in self.headers]
        table.columns.alignment = BeautifulTable.ALIGN_LEFT

        for row in self.rows:
            table.rows.append([c for c in row])

        print(table)
