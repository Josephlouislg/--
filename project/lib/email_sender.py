from contextlib import contextmanager
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender(object):
	SMTP_SERVER = ('smtp.gmail.com', 465)

	def __init__(self, user='email.sender.fpm@gmail.com', password='testsenDer'):
		self._user = user
		self._password = password

	@contextmanager
	def connection(self):
		try:
			server = smtplib.SMTP_SSL(*self.SMTP_SERVER)
			server.ehlo()
			server.login(self._user, self._password)
			yield server
		finally:
			server.close()

	def send(self, emails, subject, body):
		message = MIMEMultipart("alternative")
		message["Subject"] = subject
		message["From"] = self._user
		message["To"] = ", ".join(emails)
		msg_body = MIMEText(body, "html")
		message.attach(msg_body)
		with self.connection() as connection:
			connection.sendmail(self._user, emails, message.as_string())
