from flask import  Blueprint, request, jsonify, abort
from flask_login import current_user

from project.server import db
from project.server.model.group import Group
from project.server.group.forms import GroupForm


group_blueprint = Blueprint('group', __name__, url_prefix='/group')


@group_blueprint.route('/update', methods=['POST'])
def register():
    if not current_user:
        abort(401)
    form = GroupForm(**request.get_json())
    if form.validate():
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


@group_blueprint.route('/', methods=['GET'])
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
