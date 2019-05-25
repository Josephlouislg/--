from celery import current_app, task

from project.server import db
from project.server.model.user import User


@task(bind=True)
def send(self, emails, subject, body):
	self.app.sender.send(emails, subject, body)
