from jembe_io_examples.db import db
import sqlalchemy as sa

__all__ = ("Note",)


class Note(db.Model):
    __tablename__ = "notes"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(150), nullable=False, unique=True)
    description = sa.Column(sa.Text)

    project_id = sa.Column(sa.Integer, sa.ForeignKey("projects.id"))
    project = sa.orm.relationship("Project", backref=sa.orm.backref("notes", lazy=True))

    def __str__(self) -> str:
        return self.name

