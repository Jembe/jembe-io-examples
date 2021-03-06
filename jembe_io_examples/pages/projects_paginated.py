from math import ceil
from jembe import Component
from ..jmb import jmb
from ..db import db
from ..models import Project

__all__ = ("ProjectsPaginated",)


@jmb.page(
    "projects_paginated",
    Component.Config(url_query_params={"p": "page", "s": "search"}),
)
class ProjectsPaginated(Component):
    """
    Displays searchable and paginated list of projects.
    
    @jmb.page decorator, configures "page" and "search" state variables 
    to be used as query parameters "p" and "s" when building url.
    """

    page_size = 10

    def __init__(self, search: str = "", page: int = 0):
        """Defines "search" and "page" state variables"""
        super().__init__()

    def display(self):
        self.projects = db.session.query(Project).order_by(Project.id.desc())

        # apply search filter
        if self.state.search != "":
            self.projects = self.projects.filter(
                Project.name.ilike("%{}%".format(self.state.search))
            )

        # apply pagination
        self.total_records = self.projects.count()
        self.total_pages = ceil(self.total_records / self.page_size)
        if self.state.page > self.total_pages - 1:
            self.state.page = self.total_pages - 1
        if self.state.page < 0:
            self.state.page = 0
        self.start_record_index = self.state.page * self.page_size
        self.end_record_index = self.start_record_index + self.page_size
        if self.end_record_index > self.total_records:
            self.end_record_index = self.total_records
        self.projects = self.projects[self.start_record_index : self.end_record_index]

        return super().display()
