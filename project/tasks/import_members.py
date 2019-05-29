import random
from io import StringIO

from celery import task
import pandas as pd

from project.lib.user import NewUserService
from project.server import db
from project.server.model.group import MemberGroups
from project.server.model.user import User


@task(bind=True)
def import_users(self, csv_data, group_id):
    string_io = StringIO(csv_data)
    data_frame = pd.read_csv(string_io)
    for first_name, last_name, email, phone in zip(
            data_frame.first_name,
            data_frame.last_name,
            data_frame.email,
            data_frame.phone
    ):
        password = str(random.getrandbits(128))
        try:
            # user = User(
            #     email=email,
            #     password=password,
            #     first_name=first_name,
            #     last_name=last_name,
            #     phone=phone,
            #     type=User.TYPE.member
            # )
            # db.session.add(user)
            # db.session.commit()
            # group_member = MemberGroups(
            #     user_id=user.id,
            #     group_id=group_id
            # )
            # db.session.add(group_member)
            # db.session.commit()
            user = db.session.query(User).filter(User.email == email).first()
            NewUserService.send_confirmation_member_email_msg(user=user, password=password)
            print("dasdsadsdd")
        except Exception as e:
            raise e
