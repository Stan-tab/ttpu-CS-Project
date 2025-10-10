from .dictioanary import sentences
from dbPeewee.schema import db, User, Audio
from aiogram.filters.callback_data import CallbackData

userInChange = {}


def desiredSentence(lang, pathArr):
    desiredSentence = sentences.get(lang)
    if not bool(sentences.get(lang)):
        desiredSentence = sentences.get("en")
    for i in range(len(pathArr)):
        desiredSentence = desiredSentence.get(pathArr[i])
    if not isinstance(desiredSentence, str):
        raise Exception("Message should be string type")
    return desiredSentence


def createInChangeUser(query, action):
    idContainer = query.message.voice or query.message.audio
    audioId = idContainer.file_id
    userInChange[str(query.message.chat.id)] = inChange(
        query.message.message_id, audioId, action
    )


def createCaption(audioData):
    return f"""
    Name: {audioData.name}
Tags: {", ".join(audioData.tags)}
Uses: {audioData.uses}
"""


def evaluateTags(string: str):
    return list(
        filter(
            lambda y: bool(y),
            map(lambda x: x.strip(), string.replace("\n", "").lower().split(",")),
        )
    )


def toggleDb(fn):
    def wrapper(*arg, **kwarg):
        db.close()
        db.connect()
        # print(f"{fn.__name__}, 43sub, {arg}, {kwarg}")
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


@toggleDb
def createAudioPost(audioData, username):
    isExist = Audio.findByTgid(audioData.get("audioId"))
    if bool(isExist):
        return isExist.name
    user = User.findByUsername(username)
    audio = Audio.create(
        tgId=audioData.get("audioId"),
        name=audioData.get("name"),
        user=user,
        timing=audioData.get("timing"),
        tags=audioData.get("tags"),
    )
    return False


class audioFilter:
    def __init__(self):
        pass

    def __call__(self, message):
        return bool(message.audio) or bool(message.voice)


class inChangeFilter:
    def __init__(self, action):
        self.action = action

    def __call__(self, message):
        try:
            user = userInChange[str(message.from_user.id)]
            if user.action != self.action:
                return False
        except KeyError as e:
            return False
        return {"userData": user}


class editName(CallbackData, prefix="audio"):
    action: str
    userId: int


class addTags(CallbackData, prefix="audio"):
    action: str
    userId: int


# class SetTimings(CallbackData, prefix="audio"):
#     action: str
#     userId: int


class audioData(CallbackData, prefix="audioData"):
    id: int
    action: str


class inChange:
    def __init__(self, messageId, audioId, action):
        self.messageId = messageId
        self.audioId = audioId
        self.action = action
