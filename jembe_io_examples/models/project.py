from ..db import db
import sqlalchemy as sa

__all__ = ("Project",)


class Project(db.Model):
    __tablename__ = "projects"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(150), nullable=False, unique=True)
    description = sa.Column(sa.Text)

    def __str__(self) -> str:
        return self.name

