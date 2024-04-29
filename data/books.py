import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Books(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "books"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time_for_reading = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    about = sqlalchemy.Column(sqlalchemy.Text)
    whose = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    book = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relationship("User")

    def __repr__(self):
        return f"<Job> {self.job}"
