from flask import  Blueprint, request, jsonify, abort
from flask_login import current_user

from project.server import db
from project.server.model.group import Group, MemberGroups
from project.server.model.user import User
from project.tasks.import_members import import_users


members_blueprint = Blueprint('members', __name__, url_prefix='/members')


@members_blueprint.route('/import', methods=['POST'])
def import_members():
    if not current_user or 'file' not in request.files:
        abort(401)
    file_data = request.files['file'].read().decode('utf-8')
    group = db.session.query(Group).filter(Group.author_id == current_user.id).first() or abort(404)
    import_users.delay(file_data, group.id)
    return jsonify({"errors": {}})
    if False and "form.validate()":
        group = db.session.query(Group).filter(Group.author_id == current_user.id).first()
        if not group:
            group = Group(
                group_name=form.group_name.data,
                city=form.city.data,
                author_id=current_user.id,
                budget=form.budget.data,
                currency=Group.CURRENCY.get_as_enum_by_value(int(form.currency.data)),
            )
        else:
            group.group_name = form.group_name.data
            group.city = form.city.data,
        db.session.add(group)
        db.session.commit()
        resp = {"status": "ok", "group": group.serialized()}
        return jsonify(resp)
    return jsonify({"errors": form.errors})


@members_blueprint.route('/create', methods=['POST'])
def get_group():
    if not current_user:
        abort(401)
    group = (
        db.session.query(Group)
        .filter(Group.author_id == current_user.id)
        .first()
    )
    resp = {"status": "ok", "group": group.serialized() if group else None}
    return jsonify(resp)


@members_blueprint.route('/list', methods=['GET'])
def get_list():
    members = db.session.query(User).all()
    assoc = db.session.query(MemberGroups).all()
    resp = {"status": "ok", "users": [u.serialized() for u in members], "sdads": [(i.user_id, i.group_id) for i in assoc]}
    return jsonify(resp)
