from cerberus import Validator
from sqlalchemy.sql import exists

from project.server.model.group import Group
from project.server.model.student import Student

from project.server import db


def unique_email(field, value, error):
    if db.session.query(exists().where(Student.email == value)).scalar():
        error(field, "Student with this email already exists")


def group_foreignkey(field, value, error):
    if not db.session.query(exists().where(Group.id == value)).scalar():
        error(field, "Group with this id does not exist")


student_schema = {
	'email': {'type':'string', 'validator': unique_email },
	'first_name': {"type": 'string'},
	'last_name': {"type": 'string'},
	'group_id': {'type':'integer', 'validator': group_foreignkey }
}

student_validator = Validator(student_schema)
