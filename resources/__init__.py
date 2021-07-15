import argparse
import sys


class Verb:
    def __init__(self, parent_args):
        parser = argparse.ArgumentParser(parents=[parent_args], add_help=False)
        self.argp = parser
        self.unknown_options = None

        pass

    def add_argument(self, name, required=True):
        self.argp.add_argument(f"--{name}", required=required)

    def parse_unknowns(self, unknowns):
        unknown_parser = argparse.ArgumentParser()
        for arg in unknowns:
            name = arg.split("=")[0].split(" ")[0]
            unknown_parser.add_argument(name)

        return unknown_parser.parse_known_args(sys.argv[1:])[0]

    def run(self):
        args, unknown_args = self.argp.parse_known_args(sys.argv[1:])
        self.unknown_options = self.parse_unknowns(unknowns=unknown_args)

        self.execute(**vars(args))

    def execute(self, **options):
        raise NotImplemented


class ListVerb(Verb):
    def __init__(self, parent_args):
        super().__init__(parent_args=parent_args)
        self.argp.add_argument(f"--output", required=False, default="table")
