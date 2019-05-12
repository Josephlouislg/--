from contextlib import contextmanager
import smtplib


class EmailSender(object):
	SMTP_SERVER = ('smtp.gmail.com', 465)

	def __init__(self, user='email.sender.fpm@gmail.com', password='testsenDer'):
		self._user = user
		self._password = password

	def render_msg(self, emails, subject, body):
		msg_text = f"""
		From: {self._user}
		To: {", ".join(emails)}
		Subject: {subject}

		{body}
		"""
		return msg_text

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
		msg = self.render_msg(emails, subject, body)
		with self.connection() as connection:
			connection.sendmail(self._user, emails, msg)