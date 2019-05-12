# project/server/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40)
        ]
    )
    first_name = StringField(
        'first name',
        validators=[
            DataRequired(),
            Length(min=4, max=40)
        ]
    )
    last_name = StringField(
        'last_name',
        validators=[
            DataRequired(),
            Length(min=2, max=40)
        ]
    )
    phone = StringField(
        'phone',
        validators=[
            DataRequired(),
            Length(min=2, max=40)
        ]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
