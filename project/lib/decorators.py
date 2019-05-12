from flask import jsonify as _jsonify
from flask import json

from functools import wraps


def jsonify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return _jsonify(**func(*args, **kwargs))
    return wrapper
