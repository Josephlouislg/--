import random


from flask import url_for, render_template

from project.server.model.user import User
from project.tasks.sender import send
from project.server import db, redis


class NewUserService(object):
    SERVER_NAME = 'http://localhost:81'

    @staticmethod
    def get_user_token(user):
        return f'USER_CONFIRM_TOKEN{user.id}'

    @classmethod
    def generate_confirfation_token(cls, user):
        token = str(random.getrandbits(128))
        redis.set(cls.get_user_token(user), token)
        return token

    @classmethod
    def send_confirmation_email_msg(cls, user):
        token = cls.generate_confirfation_token(user)
        confirmation_url = f"{cls.SERVER_NAME}{url_for('auth.confirm_email', token=token, user_id=user.id)}"
        body = render_template('emails/email_confirmation.html', confirmation_url=confirmation_url)
        send.delay(
            emails=(user.email,),
            subject='Підвтердження електронної адреси',
            body=body
        )

    @classmethod
    def confirm_email(cls, token, user):
        stored_token = redis.get(cls.get_user_token(user)).decode('utf-8')
        if token == stored_token:
            user.status = User.STATUS.active
            db.session.add(user)
            db.session.commit()
            return True
