from sqlalchemy import ForeignKey, Integer, Column, Table, MetaData

from project.server import db
from project.lib.types import TitledEnum, EnumInt

meta = MetaData()


class Group(db.Model):

    __tablename__ = 'group'

    class CURRENCY(TitledEnum):
        usd = 1, 'USD'
        uah = 2, 'UAH'

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

    def serialized(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "group_name": self.group_name,
            "city": self.city,
            "budget": self.budget,
            "currency": self.currency.value,
            "status": self.status.value,
        }


class MemberGroups(db.Model):

    __tablename__ = 'association_member_group'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, ForeignKey('group.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
