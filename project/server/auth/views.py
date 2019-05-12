from functools import update_wrapper

from flask import (
    render_template, Blueprint, url_for,
    redirect, flash, request, jsonify
)
from flask_login import login_user, logout_user, login_required
from flask import jsonify


from project.server import bcrypt, db
from project.server.model.user import User
from project.server.auth.forms import LoginForm, RegisterForm


auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['POST'])
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

        return jsonify({"status": "ok", "user_id": user.id})

    return jsonify({"errors": form.errors})


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('auth.members'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@auth_blueprint.route('/members')
@login_required
def members():
    return render_template('user/members.html')


@auth_blueprint.route('/users')
def users():
    users_emails = [user.email for user in User.query.all()]
    return jsonify({"users_emails": users_emails })


@auth_blueprint.route('/users/<int:user_id>')
def user_id(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user:
        return jsonify({"email": user.email })
    resp = jsonify()
    resp.status_code = 404
    return resp
