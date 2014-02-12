def get_command():
    return Command()


class Command(object):
    name = 'hello'
    help = 'just an example'

    def add_arguments(self, subparser):
        subparser.add_argument('--name')

    def execute(self, args):
        print 'Hello, %s' % args.name
