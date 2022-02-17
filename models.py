from peewee import *
import datetime
from flask_login import UserMixin
DATABASE = SqliteDatabase('whip.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE


class Pantry(Model):
    item = CharField()
    quantity = CharField()
    catergory = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE





class Spoon(Model):

        class Meta:
            database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Pantry, Spoon], safe=True)
    print("TABLES Created")
    DATABASE.close()
