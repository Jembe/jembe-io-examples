from typing import Optional

from functools import cached_property
from jembe import Component, listener, action
from ..jmb import jmb
from ..db import db
from ..models import Project
from .projects_paginated import ProjectsPaginated

__all__ = ("ProjectsEditable",)


class ProjectEdit(Component):
    """Displays edit form and save changes to database"""

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
        """
            Saves changes to database.

            Actions can be called directly from html,
            similary to changing state variables
        """
        if self.state.name != "":
            self.project.name = self.state.name
            self.project.description = self.state.description
            db.session.commit()
            self.emit("save", project=self.project)
            # when an action returns False 
            # component will not be redisplayed even if 
            # state variables are changed
            return False
        self.error = "Name is required"

    @action
    def cancel(self):
        self.emit("cancel")
        return False

    def display(self):
        if self.state.name is None:
            # when displaed for the first time initialise name and description
            self.state.name = self.project.name
            self.state.description = self.project.description
        return super().display()


@jmb.page(
    "projects_editable", Component.Config(components={"edit": ProjectEdit}),
)
class ProjectsEditable(ProjectsPaginated):
    """
    Extends existing ProjectsPaginated component
    to add support for displaying "edit" subcomponent.
    
    @jmb.page decorators add "ProjectEdit"  as "edit" subcomponent.
    """

    def __init__(
        self, search: str = "", page: int = 0, display_mode: Optional[str] = None
    ):
        """display_mode: defines if project list or edit component are displayed"""
        super().__init__(search=search, page=page)
        if (
            display_mode is not None
            and display_mode not in self._config.components.keys()
        ):
            display_mode = None

    @listener(event="_display", source="./edit")
    def on_display_edit(self, event):
        """When "edit" subcomponent is displayed update display_mode"""
        self.state.display_mode = "edit"

    @listener(event=["cancel", "save"], source="./edit")
    def on_child_save_or_cancel(self, event):
        """When "edit" subcomponent emits "save" or "cancel" update display_mode"""
        self.state.display_mode = None

    def display(self):
        if self.state.display_mode is not None:
            # no need to query database and recalculate pagination
            # if only edit component is displayed
            return self.render_template()
        else:
            return super().display()

