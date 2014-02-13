from launchpadlib import launchpad

from . import data

def new_connection():
    lp = launchpad.Launchpad.login_anonymously('hoke', 'production',
                                               version='devel')
    return Connection(lp)


class Connection(object):
    def __init__(self, lp):
        self.lp = lp

    def get_project(self, project_name):
        project = self.lp.projects[project_name]
        return Project(project)


class Project(object):
    def __init__(self, lp_project):
        self.lp_project = lp_project

    def get_blueprints(self):
        for bp in self.lp_project.valid_specifications:
            raw = data.RawBlueprint(
                approver=self._get_person(bp.approver),
                assignee=self._get_person(bp.assignee),
                completer=self._get_person(bp.completer),
                date_completed=bp.date_completed,
                date_created=bp.date_created,
                date_started=bp.date_started,
                definition_status=bp.definition_status,
                direction_approved=bp.direction_approved,
                drafter=self._get_person(bp.drafter),
                has_accepted_goal=bp.has_accepted_goal,
                http_etag=bp.http_etag,
                implementation_status=bp.implementation_status,
                information_type=bp.information_type,
                is_complete=bp.is_complete,
                is_started=bp.is_started,
                lifecycle_status=bp.lifecycle_status,
                milestone=self._get_milestone(bp.milestone),
                name=bp.name,
                owner=self._get_person(bp.owner),
                priority=bp.priority,
                self_link=bp.self_link,
                specification_url=bp.specification_url,
                starter=self._get_person(bp.starter),
                summary=bp.summary,
                target=self._get_project(bp.target),
                title=bp.title,
                web_link=bp.web_link,
                whiteboard=bp.whiteboard,
                workitems_text=bp.workitems_text,
            )
            yield raw

    def _get_person(self, person):
        if person is None:
            return None
        return person.display_name

    def _get_project(self, project):
        if project is None:
            return None
        return project.display_name

    def _get_milestone(self, milestone):
        if milestone is None:
            return None
        return milestone.name
