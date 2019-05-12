from celery import current_app, task

from project.server import db
from project.server.model.user import User

@task(bind=True)
def send(self, a):
	users = db.session.query(User).all()
	print(users)