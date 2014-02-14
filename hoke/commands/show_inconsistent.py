from .. import models
from .. import states


def get_command():
    return Command()


class Command(object):
    name = 'inconsistent'
    help = ('List inconsistent blueprints')

    def add_arguments(self, parser):
        pass

    def execute(self, hoke_db, args):
        bps_and_reasons = self.get_inconsistent_bps_and_reasons(hoke_db)
        bps_and_reasons.sort(key=lambda x: x[0].date_created)
        self.display(bps_and_reasons)

    def get_inconsistent_bps_and_reasons(self, hoke_db):
        bps_and_reasons = []
        for raw_bp in hoke_db.list_blueprints():
            bp = models.blueprint_from_raw(raw_bp)
            consistency_checks = states.get_consistency_checks()
            failed_checks = []
            for check in consistency_checks:
                if not check.check(bp):
                    failed_checks.append(check)
            if len(failed_checks) > 0:
                bps_and_reasons.append((bp, failed_checks))
        return bps_and_reasons

    def display(self, bps_and_reasons):
        count = len(bps_and_reasons)
        print "There are {} inconsistent blueprints".format(count)
        print
        first = True
        for bp, checks in bps_and_reasons:
            if first:
                first = False
            else:
                print
            print u"{}: {}".format(bp.title, bp.url)
            for check in checks:
                print "  * {}".format(check.reason)

        print
        print "Displayed {} inconsistent blueprints".format(count)
