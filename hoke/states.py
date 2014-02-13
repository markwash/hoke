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
            age = datetime.date.now() - bp.date_tagged
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
