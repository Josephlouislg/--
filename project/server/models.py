import datetime
import importlib
import os

from flask import current_app

from project.server import db, bcrypt


MODELS_DIRECTORY = "project/server/model"
EXCLUDE_FILES = ["__init__.py"]

def import_models():
    for dir_path, dir_names, file_names in os.walk(MODELS_DIRECTORY):
        for file_name in file_names:
            if file_name.endswith("py") and not file_name in EXCLUDE_FILES:
                file_path_wo_ext, _ = os.path.splitext((os.path.join(dir_path, file_name)))
                module_name = file_path_wo_ext.replace(os.sep, ".")
                importlib.import_module(module_name)
import_models()