import datetime
import re


def blueprint_from_raw(raw_bp):
    tags = get_whiteboard_tags(raw_bp)
    tags.sort(key=lambda x: x[1])

    if len(tags) == 0:
        tag = None
        date_tagged = None
    else:
        tag, date_tagged = tags[-1]
        tag = tag.lower()
        if tag == 'untagged':
            tag = None

    return Blueprint(
        name=raw_bp.name,
        title=raw_bp.title,
        url=raw_bp.web_link,
        milestone=raw_bp.milestone,
        date_created=raw_bp.date_created,
        date_tagged=date_tagged,
        tag=tag,
        assignee=raw_bp.assignee,
        owner=raw_bp.owner,
        definition_approved=raw_bp.definition_status == 'Approved',
        direction_approved=raw_bp.direction_approved,
        summary=raw_bp.summary,
    )


def get_whiteboard_tags(raw_bp):
    if raw_bp.whiteboard is None:
        return []

    tag_pattern = re.compile(
        '^\s*(?P<tagger>\S+)\s+(?P<tag>\S+)'
        '\s+(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})\s*$'
    )
    tags = []
    for line in raw_bp.whiteboard.split('\n'):
        match = tag_pattern.match(line)
        if not match:
            continue
        date_params = [int(x) for x in match.group('year', 'month', 'day')]
        date = datetime.date(*date_params)
        tag = match.group('tag')
        tags.append((tag, date))
    tags.reverse()
    return tags


class Blueprint(object):
    def __init__(self, name, title, url, milestone,
                 date_created, date_tagged, tag,
                 assignee, owner,
                 definition_approved, direction_approved,
                 summary):
            self.name = name
            self.title = title
            self.url = url
            self.milestone = milestone
            self.date_created = date_created
            self.date_tagged = date_tagged
            self.tag = tag
            self.assignee = assignee
            self.owner = owner
            self.definition_approved = definition_approved
            self.direction_approved = direction_approved
            self.summary = summary
