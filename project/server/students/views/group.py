from flask import (
    Blueprint, url_for,
    redirect, request, jsonify
)
from project.server import db

from project.server.model.group import Group
from project.server.students.forms.group import group_validator


bp = Blueprint('group', __name__, url_prefix='/groups')


@bp.route('/create_group', methods=['POST'])
def add_group():
    if group_validator.validate(request.json):
        group = Group(**group_validator.document)
        db.session.add(group)
        db.session.commit()

        return jsonify(group.serialize())
    resp = jsonify({"errors": group_validator.errors})
    resp.status_code = 422
    return resp


@bp.route('/group_list', methods=['GET'])
def group_list():
	groups = Group.query.all()
	return jsonify([group.serialize() for group in groups])


@bp.route('/group/<int:group_id>')
def group_id(group_id: int):
    group = Group.query.filter(Group.id == group_id).first()
    if group:
        return jsonify(group.serialize())
    resp = jsonify()
    resp.status_code = 404
    return resp