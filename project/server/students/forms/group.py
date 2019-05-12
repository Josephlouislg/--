from cerberus import Validator
from sqlalchemy.sql import exists

# from project.server.model.group import Group
# from project.server.model.fuc import Fuc

from project.server import db


def unique_name(field, value, error):
    if db.session.query(exists().where(Group.name == value)).scalar():
        error(field, "Group with this name already exists")


def fuc_foreignkey(field, value, error):
    if not db.session.query(exists().where(Fuc.id == value)).scalar():
        error(field, "faculty with this id does not exist")


group_schema = {
	'name': {'type':'string', 'validator': unique_name },
	'fuc_id': {'type':'integer', 'validator': fuc_foreignkey }
}

group_validator = Validator(group_schema)
