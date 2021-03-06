import collections


RawBlueprint = collections.namedtuple(
    'RawBlueprint',
    [
        'approver',
        'assignee',
        'completer',
        'date_completed',
        'date_created',
        'date_started',
        'definition_status',
        'direction_approved',
        'drafter',
        'has_accepted_goal',
        'http_etag',
        'implementation_status',
        'information_type',
        'is_complete',
        'is_started',
        'lifecycle_status',
        'milestone',
        'name',
        'owner',
        'priority',
        'self_link',
        'specification_url',
        'starter',
        'summary',
        'target',
        'title',
        'web_link',
        'whiteboard',
        'workitems_text',
    ],
)
