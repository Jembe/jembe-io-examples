from jembe import config, Component
from ..jmb import jmb
from ..components import (
    CPage,
    CCrudListRecords,
    CEdit,
    FormBase,
    CView,
    CCreate,
    CDelete,
)
from ..db import db
from ..models import Project, Note
from wtforms import validators as v, StringField, TextAreaField, SelectField
import sqlalchemy as sa

__all__ = ("DemoReusableComponents",)


class ProjectForm(FormBase):
    """Defines project form using wtforms library"""
    name = StringField(
        validators=[v.DataRequired(), v.Length(max=Project.name.type.length)]
    )
    description = TextAreaField()

    def mount(self, component: "Component") -> "FormBase":
        if isinstance(component, CView):
            # disable all fields when form is used in view component
            self.disable_field(self.name)
            self.disable_field(self.description)
        return super().mount(component)


@config(
    CCrudListRecords.Config(
        # database engine
        db=db,
        # db query to list records
        query=sa.orm.Query([Project.id, Project.name]).order_by(Project.id.desc()),
        # search condition to be add to query
        search_filter=lambda search: Project.name.ilike("%{}%".format(search)),
        # links in component header
        actions=[lambda self: ("Create", self.component("create"))],
        # links for every record in list
        record_actions=[
            lambda self, record: ("View", self.component("view", id=record.id)),
            lambda self, record: ("Edit", self.component("edit", id=record.id)),
            lambda self, record: ("Delete", self.component("delete", id=record.id)),
        ],
        # subcomonents and its configuration
        components={
            "edit": (CEdit, CEdit.Config(db=db, model=Project, form=ProjectForm)),
            "create": (CCreate, CCreate.Config(db=db, model=Project, form=ProjectForm)),
            "view": (CView, CView.Config(db=db, model=Project, form=ProjectForm)),
            "delete": (CDelete, CDelete.Config(db=db, model=Project)),
        },
    )
)
class CListProjects(CCrudListRecords):
    pass


class NoteForm(FormBase):
    name = StringField(
        validators=[v.DataRequired(), v.Length(max=Project.name.type.length)]
    )
    description = TextAreaField()
    project_id = SelectField("Project", coerce=int)

    def mount(self, component: "Component") -> "FormBase":
        if isinstance(component, CView):
            self.disable_field(self.name)
            self.disable_field(self.description)
            self.disable_field(self.project_id)
            # displays only selected project inside view component
            self.project_id.choices = [
                (p.id, p.name)
                for p in db.session.query(Project).filter(
                    Project.id == self.project_id.data
                )
            ]
        else:
            # add projects in select project field
            self.project_id.choices = [
                (p.id, p.name) for p in db.session.query(Project)
            ]
        return super().mount(component)


@config(
    CCrudListRecords.Config(
        db=db,
        query=(
            sa.orm.Query(
                [
                    Note.id,
                    Note.name,
                    sa.sql.func.substr(Project.name, 1, 25).label("project"),
                ]
            )
            .join(Note.project)
            .order_by(Note.id.desc())
        ),
        search_filter=lambda search: Note.name.ilike("%{}%".format(search)),
        actions=[lambda self: ("Create", self.component("create"))],
        record_actions=[
            lambda self, record: ("View", self.component("view", id=record.id),),
            lambda self, record: ("Edit", self.component("edit", id=record.id),),
            lambda self, record: ("Delete", self.component("delete", id=record.id),),
        ],
        components={
            "edit": (CEdit, CEdit.Config(db=db, model=Note, form=NoteForm)),
            "create": (CCreate, CCreate.Config(db=db, model=Note, form=NoteForm),),
            "view": (CView, CView.Config(db=db, model=Note, form=NoteForm)),
            "delete": (CDelete, CDelete.Config(db=db, model=Note)),
        },
    )
)
class CListNotes(CCrudListRecords):
    pass


@jmb.page(
    "demo_reusable",
    CPage.Config(components={"projects": CListProjects, "notes": CListNotes}),
)
class DemoReusableComponents(CPage):
    pass
