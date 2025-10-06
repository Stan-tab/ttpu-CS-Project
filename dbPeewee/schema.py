from peewee import *
from playhouse.postgres_ext import ArrayField
from playhouse.db_url import connect
from os import getenv
from dotenv import load_dotenv

load_dotenv()
DATABASE = getenv("DATABASE")
db = connect(DATABASE)


class BaseModel(Model):
    class Meta:
        database = db
        ordered_by = id


class User(BaseModel):
    id = PrimaryKeyField(unique=True)
    username = CharField(unique=True)
    telegram_id = FixedCharField()

    @staticmethod
    def list():
        query = User.select()
        for row in query:
            print(row.id, row.username, row.telegram_id)

    @staticmethod
    def findByUsername(username):
        try:
            user = User.select().where(User.username == username).get()
        except User.DoesNotExist:
            user = None
        return user


class Audio(BaseModel):
    tgId = CharField()
    name = CharField()
    user = ForeignKeyField(User, backref="audio")
    timing = ArrayField(CharField)
    tags = ArrayField(CharField)
    uses = IntegerField(default=0)

    @staticmethod
    def updateNameByTgid(id, name):
        query = Audio.update(name=name).where(Audio.tgId == id)
        query.execute()
        return Audio.get(Audio.tgId == id)


if __name__ == "__main__":
    db.connect()
    # db.drop_tables([User, Audio])
    db.create_tables([User, Audio])
    print("Tables 'User' and 'Audio' created successfully.")
    db.close()
