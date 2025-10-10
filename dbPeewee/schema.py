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
    tgId = CharField(unique=True)
    name = CharField()
    user = ForeignKeyField(User, backref="audio")
    timing = ArrayField(CharField)
    tags = ArrayField(CharField)
    uses = IntegerField(default=0)

    @staticmethod
    def updateDataByTgid(id, userName, name=None, timing=None, tags=[]):
        user: User = User.findByUsername(userName)
        initialData: Audio = Audio.get(Audio.tgId == id, Audio.user == user)
        name = name or initialData.name
        timing = timing or initialData.timing
        tags = tags + initialData.tags
        query = Audio.update(name=str(name).lower(), timing=timing, tags=tags).where(
            Audio.tgId == id, Audio.user == user
        )
        query.execute()
        return Audio.get(Audio.tgId == id, Audio.user == user)

    @staticmethod
    def findByTgid(tgId):
        try:
            audio = Audio.select().where(Audio.tgId == tgId).get()
        except Audio.DoesNotExist:
            audio = None
        return audio
    
    @staticmethod
    def findByid(id):
        try:
            audio = Audio.select().where(Audio.id == id).get()
        except Audio.DoesNotExist:
            audio = None
        return audio

    @staticmethod
    def getAudioByName(name: str):
        try:
            rawAudio = Audio.select().order_by(Audio.uses)
            audio = list(
                filter(
                    lambda aud: (name in aud.name) or (Audio.inArray(name, aud.tags)),
                    rawAudio,
                )
            )
        except Audio.DoesNotExist as e:
            audio = None
        return audio

    @staticmethod
    def inArray(data, arr):
        for i in arr:
            if data in i:
                return True
        return False
    
    @staticmethod
    def getAudioByUsername(username):
        user = User.findByUsername(username)
        audios = Audio.select().where(Audio.user == user)
        return audios


if __name__ == "__main__":
    db.connect()
    # db.drop_tables([User, Audio])
    db.create_tables([User, Audio])
    print("Tables 'User' and 'Audio' created successfully.")
    db.close()
