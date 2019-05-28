from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError

from project.server.model.group import Group


def validate_currency(form, field):
    if not Group.CURRENCY.get_as_enum_by_value(int(field.data)):
        raise ValidationError('Обрана некоректна валюта')


class GroupForm(FlaskForm):
    group_name = StringField(
        'first name',
        validators=[
            DataRequired(message="Ім'я класу обов'язкове"),
            Length(min=4, max=40)
        ]
    )
    city = StringField(
        'city',
        validators=[
            DataRequired(message="Місто класу обов'язкове"),
            Length(min=2, max=40)
        ]
    )
    budget = IntegerField('budget', default=0)
    currency = IntegerField(
        'currency',
        validators=[
            DataRequired(),
            validate_currency
        ]
    )
