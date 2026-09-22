import argparse

from inspector.core.creator import Creator
from inspector.core.engine import Engine


def main():

    engine = Engine()

    parser = argparse.ArgumentParser(
        prog="inspector",
        description="Inspector CLI - Auditor Universal"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list")
    sub.add_parser("make-agent").add_argument("name")

    # Registrar automáticamente todos los agentes
    for agent in engine.registry.list():
        sub.add_parser(agent)

    args = parser.parse_args()

    if args.command == "list":
        for agent in engine.registry.list():
            print(agent)
        return

    if args.command == "make-agent":
        Creator().create(args.name)
        return

    if args.command:
        engine.run(args.command)
        return

    parser.print_help()


if __name__ == "__main__":
    main()