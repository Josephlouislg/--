# project/server/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(
        'Email Address', [
            DataRequired(message="Це поле обов'язкове"),
            Email(message='Ця електронна адреса не є коректною')
        ]
    )
    password = PasswordField('Password', [DataRequired(message="Це поле обов'язкове")])


class RegisterForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message="Це поле обов'язкове"),
            Email(message='Ця електронна адреса не є коректною'),
            Length(min=4, max=40, message="Електронна адреса повинна бути від 4-ох до 40-а символів")
        ]
    )
    first_name = StringField(
        'first name',
        validators=[
            DataRequired(message="Це поле обов'язкове"),
            Length(min=4, max=40, message="Ім'я повинно бути від 4-ох до 40-а символів")
        ]
    )
    last_name = StringField(
        'last_name',
        validators=[
            DataRequired(message="Це поле обов'язкове"),
            Length(min=2, max=40, message='Прізвище повинно бути від 2-ох до 40-а символів')
        ]
    )
    phone = StringField(
        'phone',
        validators=[
            DataRequired(message="Це поле обов'язкове"),
            Length(min=8, max=40, message='Номер телефону повинен бути від 8-ох до 20-а символів')
        ]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(message="Це поле обов'язкове"), Length(
            min=6,
            max=255,
            message='Пароль повинен бути від 6-ох до 255-а символів'
        )]
    )
