from peewee import *
import datetime

DATABASE = SqliteDatabase('whip.sqlite')


class Pantry(Model):
    item = CharField()
    quanity = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Pantry], safe=True)
    print("TABLES Created")
    DATABASE.close()
