from .. import models
from .. import states

from .. import display


def get_command():
    return Command()


class Command(object):
    name = 'infowait'
    help = ('List blueprints waiting for more info')

    def add_arguments(self, parser):
        pass

    def execute(self, hoke_db, args):
        bps = self.get_bps(hoke_db)
        bps.sort(key=lambda x: x.date_tagged)
        self.display(bps)

    def get_bps(self, hoke_db):
        bps = []
        for raw_bp in hoke_db.list_blueprints():
            bp = models.blueprint_from_raw(raw_bp)
            check = states.get_infowait_check()
            if check.check(bp):
                bps.append(bp)
        return bps

    def display(self, bps):
        print "There are {} blueprints that need more info".format(len(bps))
        print
        first = True
        for bp in bps:
            if first:
                first = False
            else:
                print
            print u"{}:".format(bp.title)
            print u"  Owner: {}".format(bp.owner)
            print u"  Date Tagged: {}".format(
                bp.date_tagged.isoformat())
            print u"  URL: {}".format(bp.url)
        print
        print "Displayed {} new blueprints".format(len(bps))
