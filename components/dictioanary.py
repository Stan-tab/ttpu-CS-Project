from aiogram import html

sentences = {
    "en": {
        "greeting": f"Hello $|.\nWelcome to {html.italic('funny')} audio bot 😎.\nI hope you will love it ❤️.\nIf you want to know how bot works enter /help",
        "help": f"This bot is made to entertain you 🤪.\nYou can send audio to me and i save it for all users 😍.\n Btw, you can call me in any chat and i will show audio that i have 😉.\n Let's begin 🎉.",
        "myAudio":"Show my audio🎧",
        "caption": {
            "name":"Name",
            "tags":"Tags🎬",
            "uses":"Uses📈",
        },
        "set": {
            "editName":"Change the name",
            "addTag":"Add tags",
        },
        "editName":"Enter the new name:",
        "addTag":"Add tags\nExample:\nfun, modern, cool",
        "errExist": "We already have this",
        "errNoAudio": "Sorry, we could'nt find your audios\nBut you can upload if you wish",
        "showAudios": "Your audios",
    },
    "ru": {
        "greeting": f"Привет $|.\nДобро пожаловать в {html.italic('забавный')} аудиобот 😎.\nНадеюсь, вам понравится ❤️\nЕсли вы хотите узнать, как работает бот, введите /help",
        "help": f"Этот бот создан, чтобы развлекать вас 🤪.\nВы можете отправлять мне аудио, и я сохраню его для всех пользователей 😍.\nTaкже, вы можете позвонить мне в любой чат, и я покажу вам мои аудио 😉.\nДавайте начнём 🎉.",
        "myAudio":"Показать мое аудио🎧",
        "caption": {
            "name":"Имя",
            "tags":"Тэги🎬",
            "uses":"Использований📈",
        },
        "set": {
            "editName":"Изменить имя",
            "addTag":"Добавить теги",
        },
        "editName":"Введите новое имя",
        "addTag":"Добавить теги\nПример:\nвеселый, современно, круто",
        "errExist": "У нас уже есть это аудио",
        "errNoAudio": "Извините, мы не смогли найти ваши аудиозаписи.\nНо вы можете загрузить их, если хотите.",
        "showAudios": "Ваши аудио",
    },
}


def useSentences(sent, inputArray):
    dividedSentence = sent.split("$|")
    dsLength = len(dividedSentence)
    if dsLength - 1 != len(inputArray):
        raise Exception("Too many or not enough input words")
    for i in range(len(inputArray)):
        dividedSentence.insert(i + 1, inputArray[i])
    return "".join(dividedSentence)
