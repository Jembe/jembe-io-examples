from jembe import config
from jembe_io_examples.jmb import jmb
from jembe_io_examples.components import CPage, CListRecords, CEdit, FormBase
from jembe_io_examples.db import db
from jembe_io_examples.models import Project
from wtforms import validators as v, StringField, TextAreaField
import sqlalchemy as sa

__all__ = ("ProjectsReusablePage",)


class ProjectForm(FormBase):
    name = StringField(
        validators=[v.DataRequired(), v.Length(max=Project.name.type.length)]
    )
    description = TextAreaField()


@config(CEdit.Config(db=db, form=ProjectForm, model=Project,))
class CEditProject(CEdit):
    pass


@config(
    CListRecords.Config(
        db=db,
        query=sa.orm.Query([Project.id, Project.name, Project.description]).order_by(
            Project.id.desc()
        ),
        search_filter=lambda search: Project.name.ilike("%{}%".format(search)),
        record_actions=[lambda self, record: ("Edit", self.component("edit", id=record.id))],
        components={"edit": CEditProject},
    )
)
class CListProjects(CListRecords):
    pass


@jmb.page("projects_reusable", CPage.Config(components={"projects": CListProjects}))
class ProjectsReusablePage(CPage):
    pass
