from flask import (
    Blueprint, url_for,
    redirect, request, jsonify
)
from project.server import db

# from project.server.model.university import University
from project.server.students.forms.university import university_validator


bp = Blueprint('university', __name__, url_prefix='/university')


@bp.route('/create_university', methods=['POST'])
def add_university():
    if university_validator.validate(request.json):
        university = University(
            **university_validator.document
        )
        db.session.add(university)
        db.session.commit()

        return jsonify(university.serialize())
    resp = jsonify({"errors": university_validator.errors})
    resp.status_code = 422
    return resp


@bp.route('/universities', methods=['GET'])
def university_list():
	universities = University.query.all()
	return jsonify([university.serialize() for university in universities])


@bp.route('/universities/<int:university_id>')
def university_id(university_id: int):
    university = University.query.filter(University.id == university_id).first()
    if university:
        return jsonify(university.serialize())
    resp = jsonify()
    resp.status_code = 404
    return resp