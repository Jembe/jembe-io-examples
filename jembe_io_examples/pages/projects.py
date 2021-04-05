from jembe import Component
from jembe_io_examples.jmb import jmb
from jembe_io_examples.db import db
from jembe_io_examples.models import Project

__all__ = ("Projects",)


@jmb.page("projects")
class Projects(Component):
    """ Displays searchable list of projects."""

    def __init__(self, search: str = ""):
        super().__init__()

    def display(self):
        self.projects = db.session.query(Project).order_by(Project.id.desc())
        if self.state.search != "":
            self.projects = self.projects.filter(
                Project.name.ilike("%{}%".format(self.state.search))
            )
        return super().display()
