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
        widths = [10 for _ in range(len(self.headers))]

        for row in self.rows:
            for index, val in enumerate(row):
                str_len = len(str(val))

                if str_len > widths[index]:
                    widths[index] = str_len
        fmt = []

        for width in widths:
            width = min(width, 60)
            fmt.append(f"{{:<{width + 3}.{width}}}")

        fmt = "".join(fmt)
        print(fmt.format(*[h.upper() for h in self.headers]))

        for row in self.rows:
            print(fmt.format(*[str(v) for v in row]))
