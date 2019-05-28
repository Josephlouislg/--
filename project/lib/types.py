from enum import Enum

from sqlalchemy.types import SmallInteger, TypeDecorator


class EnumInt(TypeDecorator):

    impl = SmallInteger

    def __init__(self, enum, *args, **kwargs):
        self._enum = enum
        super().__init__(*args, **kwargs)

    def process_bind_param(self, enum, dialect):
        if enum is None:
            return None
        return enum.value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self._enum(value)
        return value

    def copy(self, **kw):
        return EnumInt(self._enum)


class TitledEnum(Enum):

    def __new__(cls, value, title=''):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, value, title=''):
        reserved = ('choices', 'json_choices', '_choices', '_json_choices')
        if self.name in reserved:
            raise ValueError('Illegal name: {}'.format(self.name))

        self.title = title

    @classmethod
    def choices(cls):
        """Get choices from enum

        Returns:
            list of (value, title) tuples
        """
        if not hasattr(cls, '_choices'):
            cls._choices = [(e.value, e.title) for e in cls]
        return cls._choices

    @classmethod
    def json_choices(cls, filter_func=lambda e: True):
        """Get json choices from enum

        Returns:
            list of {'value': <value>, 'title': <title>} dicts
        """
        if not hasattr(cls, '_json_choices'):
            cls._json_choices = json.dumps(
                [
                    {'value': str(e.value), 'title': e.title}
                    for e in cls if filter_func(e)]
            )
        return cls._json_choices

    @classmethod
    def as_dict(cls):
        return OrderedDict(
            [(e.name, {'value': str(e.value), 'title': e.title}) for e in cls]
        )

    @classmethod
    def get_as_enum(cls, val, default=None):
        return next((e for e in cls if e.value == val), default)

    @classmethod
    def get_as_enum_by_title(cls, title, default=None):
        return next((e for e in cls if e.title == title), default)

    @classmethod
    def get_as_enum_by_value(cls, value, default=None):
        return next((e for e in cls if e.value == value), default)
