from functools import update_wrapper

from flask import (
    render_template, Blueprint, url_for,
    redirect, flash, request, jsonify,
    abort)
from flask_login import login_user, logout_user, login_required, current_user

from project.server import bcrypt, db
from project.server.model.user import User
from project.server.auth.forms import LoginForm, RegisterForm

from project.tasks.sender import send
from project.lib.user import NewUserService

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(**request.get_json())
    if form.validate():
        user = User(
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        NewUserService.send_confirmation_email_msg(user=user)
        resp = {"status": "ok", "user": user.serialized()}
        return jsonify(resp)
    return jsonify({"errors": form.errors})


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    form = LoginForm(**data)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, data['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            resp = {"status": "ok", "user": user.serialized()}
            return jsonify(resp)
        else:
            flash('Invalid email and/or password.', 'danger')
            resp = {"status": "ok", "user": None}
            return jsonify(resp)
    return jsonify({"errors": form.errors})


@auth_blueprint.route('/user', methods=['GET'])
def get_user():
    resp = {
        "need_auth": current_user is None,
        "user": current_user.serialized() if current_user.is_authenticated else None
    }
    return jsonify(resp)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    resp = {"status": "ok"}
    return jsonify(resp)


@auth_blueprint.route('/members')
@login_required
def members():
    return render_template('user/members.html')


@auth_blueprint.route('/users')
def users():
    users_emails = [user.email for user in User.query.all()]
    return jsonify({"users_emails": users_emails })


@auth_blueprint.route('/confirm_email/<int:user_id>/<token>')
def confirm_email(user_id, token):
    user = db.session.query(User).filter(
        User.id == user_id,
        User.status == User.STATUS.email_confirmation
    ).first() or abort(404)
    NewUserService.confirm_email(token=token, user=user)
    return redirect('/')
