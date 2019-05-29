import importlib

from celery.app.task import Task
import celery

from project.lib.email_sender import EmailSender


def register_tasks(real_app):
    module_names = (
        'sender',
        'import_members',
    )
    for module_name in module_names:
        mod = importlib.import_module(__name__ + '.' + module_name)
        for name in dir(mod):
            attr = getattr(mod, name)
            if isinstance(attr, Task):
                attr.app = real_app


def init_celery(app):
    celery_app = celery.Celery(app.import_name, broker=app.config['CELERY']['broker'])
    app.config.update(SERVER_NAME='localhost:81/api', SESSION_COOKIE_DOMAIN='.localhost:81')
    celery_app.conf.update(app.config['CELERY'])
    register_tasks(celery_app)
    sender = EmailSender()
    celery_app.sender = sender
    celery_app.finalize()
    return celery_app
