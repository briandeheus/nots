#!/usr/bin/env python
import argparse
import logging
import inspect
import sys

from resources import Verb, custom
from resources.builtin import (
    system as builtin_system,
    resource as builtin_resource,
    field as builtin_field,
)

V_TO_LEVELS = {0: logging.ERROR, 1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG}
logging.basicConfig(format="[%(levelname)s] %(message)s")


def build_resources_and_verbs(skip_custom=False):
    resources = {}
    builtins = [builtin_system, builtin_resource, builtin_field]

    for builtin in builtins:
        verbs = builtin.VERBS
        for name in builtin.NAMES:
            resources[name] = verbs

    if not skip_custom:
        for resource in builtin_resource.get_resources():
            verbs = custom.VERBS
            resources[resource.name] = verbs
            resources[resource.plural] = verbs

    return resources


def run(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("verb")
    parser.add_argument("resource")
    parser.add_argument("-v", required=False, type=int, default=0)
    args = parser.parse_known_args(argv[1:])[0]

    if args.resource == "system":
        resources_and_verbs = build_resources_and_verbs(skip_custom=True)
    else:
        resources_and_verbs = build_resources_and_verbs()

    resource_list = [r for r in resources_and_verbs]

    logging.getLogger().setLevel(level=V_TO_LEVELS[args.v])
    logging.debug('Executing command "%s"', " ".join(argv[1:]))

    if args.resource not in resources_and_verbs:
        logging.error(
            'Unknown resource "%s". Valid resources are:\n%s',
            args.resource,
            "".join([f"\t- {r}\n" for r in resource_list]),
        )
        exit(1)

    verbs = resources_and_verbs[args.resource]

    if args.verb not in verbs:
        logging.error(
            'Unknown verb "%s". Valid verbs are:\n%s',
            args.verb,
            "".join([f"\t- {verb}\n" for verb in verbs]),
        )
        exit(1)

    verb = verbs[args.verb]

    if inspect.isclass(verb) and issubclass(verb, Verb):
        v = verb(argv=argv, parent_args=parser)
        v.run()
    else:
        verb()


def main():
    run(argv=sys.argv)


if __name__ == "__main__":
    main()
