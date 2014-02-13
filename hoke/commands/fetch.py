from .. import db
from .. import lp

def get_command():
    return Command()


class Command(object):
    name = 'fetch'
    help = ('Download all valid blueprints from launchpad for projects '
            'and save in a local file.')

    def add_arguments(self, parser):
        parser.add_argument('projects', nargs='+', metavar='project')
        parser.add_argument('--file', default='.hoke-db')

    def execute(self, args):
        hoke_db = db.new_db(args.file)
        launchpad = lp.new_connection()
        for project in args.projects:
            lp_project = launchpad.get_project(project)
            for bp in lp_project.get_blueprints():
                hoke_db.add_blueprint(bp)
        hoke_db.close()
