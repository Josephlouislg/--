from cerberus import Validator
from sqlalchemy.sql import exists

# from project.server.model.university import University
from project.server import db


def unique(field, value, error):
    if db.session.query(exists().where(University.name == value)).scalar():
        error(field, "University with this name already exists")


university_schema = {
	'name': {'type':'string', 'validator': unique }
}


university_validator = Validator(university_schema)
