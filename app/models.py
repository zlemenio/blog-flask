
from app import db
import datetime
from flask_login import UserMixin
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from typing import List


class Person(db.Model):
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    __tablename__ = "person_table"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    todolist: Mapped[List["TodoList"]] = relationship(back_populates="person")

    def __repr__(self):
        return f'<Person {self.username}>'


class TodoList(db.Model):
    __tablename__ = "todolist_table"
    id = db.Column(db.Integer, primary_key=True)

    category = db.Column(db.String(1000))
    description = db.Column(db.String(10000))
    status = db.Column(db.String(100))
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    person_id: Mapped[int] = mapped_column(ForeignKey("person_table.id"))
    person: Mapped["Person"] = relationship(
        back_populates="todolist", single_parent=True)
