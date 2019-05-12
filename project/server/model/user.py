import datetime

from flask import current_app

from project.server import db, bcrypt
from project.lib.types import TitledEnum, EnumInt


class User(db.Model):

    __tablename__ = 'user'

    class STATUS(TitledEnum):
        email_confirmation = 1, 'Подтверждение емейла'
        active = 2, 'Активный'
        deleted = 3, 'Удален'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    status = db.Column(EnumInt(STATUS), nullable=False, default=STATUS.email_confirmation)

    def __init__(self, email, password, *args, **kwargs):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        super().__init__(*args, **kwargs)

    @property
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}, id:{1}>'.format(self.email, self.id)
