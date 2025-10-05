from .dictioanary import sentences
from dbPeewee.schema import db, User, Audio


def desiredSentence(lang, pathArr):
    desiredSentence = sentences.get(lang)
    if not bool(sentences.get(lang)):
        desiredSentence = sentences.get("en")
    for i in range(len(pathArr)):
        desiredSentence = desiredSentence.get(pathArr[i])
    if not isinstance(desiredSentence, str):
        raise Exception("Message should be string type")
    return desiredSentence


def toggleDb(fn):
    def wrapper(*arg, **kwarg):
        db.connect()
        result = fn(*arg, **kwarg)
        db.close()
        return result

    return wrapper

@toggleDb
def createUser(username, telegram_id):
    user = User.findByUsername(username)
    if not bool(user):
        user = User.create(username=username, telegram_id=telegram_id)
    return user
