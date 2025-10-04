from aiogram import html

sentences = {
    "en": {
        "greeting": f"Hello $|.\nWelcome to {html.italic('funny')} audio bot 😎.\nI hope you will love it ❤️.\nIf you want to know how bot works enter /help"
    },
    "ru": {
        "greeting": f"Привет $|.\nДобро пожаловать в {html.italic('забавный')} аудиобот 😎.\nНадеюсь, вам понравится ❤️\nЕсли вы хотите узнать, как работает бот, введите /help"
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
