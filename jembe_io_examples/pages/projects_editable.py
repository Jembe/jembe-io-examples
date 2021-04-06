from typing import Optional

from functools import cached_property
from jembe import Component, listener, action
from jembe_io_examples.jmb import jmb
from jembe_io_examples.db import db
from jembe_io_examples.models import Project
from .projects_paginated import ProjectsPaginated

__all__ = ("ProjectsEditable",)


class ProjectEdit(Component):
    def __init__(
        self, id: int, name: Optional[str] = None, description: Optional[str] = None
    ):
        self.error = None
        super().__init__()

    @cached_property
    def project(self):
        return db.session.query(Project).get(self.state.id)

    @action
    def save(self):
        if self.state.name != "":
            self.project.name = self.state.name
            self.project.description = self.state.description
            db.session.commit()
            self.emit("save", project=self.project)
            return False
        self.error = "Name is required"

    @action
    def cancel(self):
        self.emit("cancel")
        return False

    def display(self):
        if self.state.name is None:
            # when displaed for the first time initilise name and description
            self.state.name = self.project.name
            self.state.description = self.project.description
        return super().display()


@jmb.page(
    "projects_editable", Component.Config(components={"edit": ProjectEdit}),
)
class ProjectsEditable(ProjectsPaginated):
    """Displays editable, searchable and paginated list of projects."""

    def __init__(
        self, search: str = "", page: int = 0, display_mode: Optional[str] = None
    ):
        super().__init__(search=search, page=page)
        if (
            display_mode is not None
            and display_mode not in self._config.components.keys()
        ):
            display_mode = None

    @listener(event="_display", source="./edit")
    def on_display_edit(self, event):
        self.state.display_mode = "edit"

    @listener(event=["cancel", "save"], source="./*")
    def on_child_save_or_cancel(self, event):
        self.state.display_mode = None

    def display(self):
        if self.state.display_mode is None:
            return super().display()
        else:
            # no need to query database and recalculate pagintation
            return self.render_template()

