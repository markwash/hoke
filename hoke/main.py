import argparse
from .commands import hello


def main():
    parser = get_argument_parser()
    args = parser.parse_args()
    run_command(args)


def get_argument_parser():
    argument_parser = argparse.ArgumentParser()
    subparsers = argument_parser.add_subparsers(help='commands')
    subcommands = get_subcommands()
    help_command = HelpCommand(argument_parser)
    for command in subcommands:
        subparser = subparsers.add_parser(command.name, help=command.help)
        command.add_arguments(subparser)
        subparser.set_defaults(command_obj=command)
        help_command.add(command, subparser)
    subparser = subparsers.add_parser(help_command.name, help=help_command.help)
    help_command.add_arguments(subparser)
    subparser.set_defaults(command_obj=help_command)
    help_command.add(help_command, subparser)
    return argument_parser


def get_subcommands():
    return [
        hello.get_command()
    ]


def run_command(args):
    args.command_obj.execute(args)


class HelpCommand(object):
    name = 'help'
    help = 'help with a command'

    def __init__(self, parser):
        self.parser = parser
        self.commands = []

    def add(self, command, subparser):
        self.commands.append((command, subparser))

    def add_arguments(self, subparser):
        subparser.add_argument('command', nargs='?')

    def execute(self, args):
        if args.command is None:
            self.parser.print_help()
            return
        for command, subparser in self.commands:
            if command.name == args.command:
                subparser.print_help()
                return
        else:
            print 'Command %s not recognized.' % args.command_name


