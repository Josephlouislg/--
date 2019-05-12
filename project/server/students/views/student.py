from flask import (
    Blueprint, url_for,
    redirect, request, jsonify
)
from project.server import db

from project.server.model.student import Student
from project.server.students.forms.student import student_validator


bp = Blueprint('student', __name__, url_prefix='/student')


@bp.route('/create_student', methods=['POST'])
def add_student():
    if student_validator.validate(request.json):
        fuc = Fuc(**student_validator.document)
        db.session.add(fuc)
        db.session.commit()

        return jsonify(fuc.serialize())
    resp = jsonify({"errors": student_validator.errors})
    resp.status_code = 422
    return resp


@bp.route('/student_list', methods=['GET'])
def student_list():
	students = Student.query.all()
	return jsonify([student.serialize() for student in students])


@bp.route('/student/<int:student_id>')
def student_id(student_id: int):
    student = Student.query.filter(Student.id == student_id).first()
    if student:
        return jsonify(student.serialize())
    resp = jsonify()
    resp.status_code = 404
    return resp