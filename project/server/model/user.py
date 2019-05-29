import datetime

from flask import current_app
from flask_login import UserMixin

from project.server import db, bcrypt
from project.lib.types import TitledEnum, EnumInt


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    class STATUS(TitledEnum):
        email_confirmation = 1, 'Подтверждение емейла'
        active = 2, 'Активный'
        deleted = 3, 'Удален'

    class TYPE(TitledEnum):
        admin = 1, 'Admin'
        member = 2, 'member'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    status = db.Column(EnumInt(STATUS), nullable=False, default=STATUS.email_confirmation)
    type = db.Column(EnumInt(TYPE), nullable=False, default=TYPE.admin)

    def __init__(self, email, password, *args, **kwargs):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        super().__init__(*args, **kwargs)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.status == self.STATUS.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def serialized(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "status": self.status.value,
            "is_admin": self.type == self.TYPE.admin
        }

    def __repr__(self):
        return '<User {0}, id:{1}>'.format(self.email, self.id)
