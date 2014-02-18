import sys

from .. import db

from . import show_inconsistent
from . import show_infowait
from . import show_new


def get_command():
    return Command()


class Command(object):
    name = 'show'
    help = ('List blueprints in a given state')

    def add_arguments(self, parser):
        parser.add_argument('--file', default='.hoke-db')
        subparsers = parser.add_subparsers(help='types')
        for command in self.get_subcommands():
            subparser = subparsers.add_parser(command.name, help=command.help)
            command.add_arguments(subparser)
            subparser.set_defaults(show_command_obj=command)

    def get_subcommands(self):
        return [
            show_inconsistent.get_command(),
            show_infowait.get_command(),
            show_new.get_command(),
        ]

    def execute(self, args):
        hoke_db = db.open_db(args.file)
        args.show_command_obj.execute(hoke_db, args)
        sys.stdout.flush()
