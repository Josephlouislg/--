from celery import current_app, task

from project.server import db
from project.server.model.user import User


@task(bind=True)
def send(self, a):
	self.app.sender.send(['vlad201297stetsenko@gmail.com'], 'test', 'test')