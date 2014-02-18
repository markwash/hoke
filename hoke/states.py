import datetime


class TagMustBeValid(object):
    valid_tags = [None, 'abandoned', 'rejected', 'more-info', 'wishlist']
    reason = 'invalid tag'

    def check(self, bp):
        return bp.tag in self.valid_tags


class DefinitionImpliesDirectionApproved(object):
    reason = 'definition approved but direction not approved'

    def check(self, bp):
        return bp.direction_approved or not bp.definition_approved


class AbandonedImpliesUnassigned(object):
    reason = 'abandoned but has assignee'

    def check(self, bp):
        return not bp.assignee or bp.tag != 'abandoned'


class NewImpliesNotApproved(object):
    reason = 'approved but not wishlist or targeted'

    def check(self, bp):
        if bp.tag is None and not bp.milestone:
            return not bp.direction_approved and not bp.definition_approved
        return True


class TargetedImpliesNotTagged(object):
    reason = 'targeted but still has tag'

    def check(self, bp):
        if bp.milestone:
            return bp.tag is None
        return True


class TargetedImpliesApproved(object):
    reason = 'targeted but not approved'

    def check(self, bp):
        if bp.milestone:
            return bp.direction_approved and bp.definition_approved
        return True


class TargetedImpliesAssigned(object):
    reason = 'targeted but not assigned'

    def check(self, bp):
        if bp.milestone:
            return bp.assignee
        return True


class WishlistImpliesDirectionApproved(object):
    reason = 'tagged as wishlist but direction not approved'

    def check(self, bp):
        if bp.tag == 'wishlist':
            return bp.direction_approved
        return True


class InfoWaitImpliesYoung(object):
    reason = 'waiting for information for too long'

    def check(self, bp):
        if bp.tag == 'more-info':
            age = datetime.datetime.now().date() - bp.date_tagged
            return age <= datetime.timedelta(days=14)
        return True


class RejectedImpliesNotApproved(object):
    reason = 'tagged as rejected but has been approved'

    def check(self, bp):
        if bp.tag == 'rejected':
            return not bp.direction_approved and not bp.definition_approved
        return True


class InfoWaitImpliesNotFullyApproved(object):
    reason = 'tagged more-info but definition is approved'

    def check(self, bp):
        if bp.tag == 'more-info':
            return not bp.definition_approved
        return True


def get_consistency_checks():
    return [
        TagMustBeValid(),
        TargetedImpliesNotTagged(),
        DefinitionImpliesDirectionApproved(),
        TargetedImpliesApproved(),
        TargetedImpliesAssigned(),
        AbandonedImpliesUnassigned(),
        NewImpliesNotApproved(),
        WishlistImpliesDirectionApproved(),
        InfoWaitImpliesYoung(),
        RejectedImpliesNotApproved(),
        InfoWaitImpliesNotFullyApproved(),
    ]


def get_inconsistent_check():
    return InconsistentCheck(get_consistency_checks())


class InconsistentCheck(object):
    def __init__(self, consistency_checks):
        self.checks = consistency_checks

    def check(self, bp):
        for check in self.checks:
            if not check.check(bp):
                return True
        return False


def get_new_check():
    return NewCheck()


class NewCheck(object):
    """Determine if a blueprint is in the "new" state"""

    def check(self, bp):
        return (bp.tag is None
                and not bp.milestone
                and not bp.direction_approved
                and not bp.definition_approved)


def get_infowait_check():
    return InfoWaitCheck()


class InfoWaitCheck(object):
    def check(self, bp):
        if not bp.tag == 'more-info':
            return False

        now = datetime.datetime.now().date()
        age = now - bp.date_tagged
        old = age > datetime.timedelta(days=14)
        return (not bp.milestone
                and not bp.definition_approved
                and not old)


def get_abandoned_check():
    return AbandonedCheck()


class AbandonedCheck(object):
    def check(self, bp):
        return (bp.tag == 'abandoned'
                and not bp.milestone
                and not bp.assignee
                and not (bp.definition_approved
                         and not bp.direction_approved)
        )


def get_rejected_check():
    return RejectedCheck()


class RejectedCheck(object):
    def check(self, bp):
        return (bp.tag == 'rejected'
                and not bp.milestone
                and not bp.direction_approved
                and not bp.definition_approved)


def get_targeted_check():
    return TargetedCheck()


class TargetedCheck(object):
    def check(self, bp):
        return (bp.tag is None
                and bp.milestone
                and bp.direction_approved
                and bp.definition_approved
                and bp.assignee)


def get_wishlist_check():
    return WishlistCheck()


class WishlistCheck(object):
    def check(self, bp):
        return (bp.tag == 'wishlist'
                and not bp.milestone
                and bp.direction_approved)


def get_all_checks():
    all_checks = AllChecks()
    checklist = [
        ('new', get_new_check()),
        ('inconsistent', get_inconsistent_check()),
        ('infowait', get_infowait_check()),
        ('abandoned', get_abandoned_check()),
        ('rejected', get_rejected_check()),
        ('targeted', get_targeted_check()),
        ('wishlist', get_wishlist_check()),
    ]
    for name, check in checklist:
        all_checks.add_check(name, check)
    return all_checks


class AllChecks(object):
    def __init__(self):
        self.checks = {}

    def add_check(self, name, check):
        self.checks[name] = check

    def get_state(self, bp):
        state = set()
        for name, check in self.checks.iteritems():
            if check.check(bp):
                state.add(name)
        return frozenset(state)
