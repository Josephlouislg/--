import random

from flask import  Blueprint, request, jsonify, abort
from flask_login import current_user

from project.lib.user import NewUserService
from project.server import db
from project.server.auth.forms import RegisterForm
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
    return jsonify({"status": 'ok'})


@members_blueprint.route('/create', methods=['POST'])
def create_member():
    if not current_user:
        abort(401)
    group = db.session.query(Group).filter(Group.author_id == current_user.id).first() or abort(404)
    password = str(random.getrandbits(128))
    form = RegisterForm(password=password, **request.get_json())
    if form.validate():
        user = User(
            email=form.email.data,
            password=password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data
        )
        db.session.add(user)
        db.session.commit()
        member_group = MemberGroups(group_id=group.id, user_id=user.id)
        db.session.add(member_group)
        db.session.commit()
        NewUserService.send_confirmation_member_email_msg(user=user, password=password)
        resp = {"status": "ok", "user": user.serialized()}
        return jsonify(resp)
    return jsonify({"errors": form.errors})


@members_blueprint.route('/list', methods=['GET'])
def get_list():
    members = db.session.query(User).all()
    assoc = db.session.query(MemberGroups).all()
    resp = {"status": "ok", "users": [u.serialized() for u in members], "sdads": [(i.user_id, i.group_id) for i in assoc]}
    return jsonify(resp)
