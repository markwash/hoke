from .. import db
from .. import models
from .. import states

def get_command():
    return Command()


class Command(object):
    name = 'status'
    help = ('Give counts of blueprints in each state')

    def add_arguments(self, parser):
        parser.add_argument('--file', default='.hoke-db')

    def execute(self, args):
        hoke_db = db.open_db(args.file)
        all_checks = states.get_all_checks()
        counter = {}
        for bp in self.get_bps(hoke_db):
            state = all_checks.get_state(bp)
            if state not in counter:
                counter[state] = 0
            counter[state] += 1
        hoke_db.close()
        for state, count in counter.items():
            if len(state) == 0:
                print '{} unknown'.format(count)
            elif len(state) == 1:
                print '{} {}'.format(count, list(state)[0])
            else:
                print '{} in combination state {}'.format(count, list(state))

    def get_bps(self, hoke_db):
        for raw_bp in hoke_db.list_blueprints():
            yield models.blueprint_from_raw(raw_bp)
