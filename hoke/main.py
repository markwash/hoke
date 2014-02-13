import argparse

from .commands import fetch
from .commands import hello
from .commands import show


def main():
    parser = get_argument_parser()
    args = parser.parse_args()
    run_command(args)


def get_argument_parser():
    argument_parser = argparse.ArgumentParser()
    subparsers = argument_parser.add_subparsers(help='commands')
    for command in get_subcommands():
        subparser = subparsers.add_parser(command.name, help=command.help)
        command.add_arguments(subparser)
        subparser.set_defaults(command_obj=command)
    return argument_parser


def get_subcommands():
    return [
        hello.get_command(),
        fetch.get_command(),
        show.get_command(),
    ]


def run_command(args):
    args.command_obj.execute(args)
