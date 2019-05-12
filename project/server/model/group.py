import datetime

from flask import current_app
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, foreign

from project.server import db, bcrypt
from project.lib.types import TitledEnum, EnumInt

class Group(db.Model):

    __tablename__ = 'group'

    class CURRENCY(TitledEnum):
        usd = 1, '$'
        uah = 2, '$'

    class STATUS(TitledEnum):
        active = 1, 'Активный'
        deleted = 2, 'Удален'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, ForeignKey('user.id'))
    # author = relationship('user')
    group_name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    currency = db.Column(EnumInt(CURRENCY), nullable=False, default=CURRENCY.uah)
    status = db.Column(EnumInt(STATUS), nullable=False, default=STATUS.active)