from .dictioanary import sentences


def desiredSentence(lang, pathArr):
    desiredSentence = sentences.get(lang)
    if not bool(sentences.get(lang)):
        desiredSentence = sentences.get("en")
    for i in range(len(pathArr)):
        desiredSentence = desiredSentence.get(pathArr[i])
    if not isinstance(desiredSentence, str):
        raise Exception("Message should be string type")
    return desiredSentence
