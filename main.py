from dotenv import load_dotenv
from os import getenv
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import aiogram.filters as filters
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineQuery,
    InlineQueryResultCachedVoice,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InputMediaAudio,
)
from components.dictioanary import useSentences
from components.subFunctions import *
from uuid import uuid4

load_dotenv()
TOKEN = getenv("API_TOKEN")
dp = Dispatcher()


async def main():
    global bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


async def sendAudioAnswer(message, audioId, caption, reply_markup):
    if message.voice:
        await message.answer_voice(
            voice=audioId,
            caption=caption,
            reply_markup=reply_markup,
        )
    elif message.audio:
        await message.answer_audio(
            audio=audioId,
            caption=caption,
            reply_markup=reply_markup,
        )


def createSetAudioButtons(userId):
    return [
        [
            InlineKeyboardButton(
                text="Edit name",
                callback_data=editName(
                    userId=userId,
                    action="edit_name",
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="Add tags",
                callback_data=addTags(
                    userId=userId,
                    action="add_tags",
                ).pack(),
            )
        ],
        # [
        #     InlineKeyboardButton(
        #         text="Change timing",
        #         callback_data=SetTimings(
        #             userId=userId,
        #             action="timing",
        #         ).pack(),
        #     )
        # ],
    ]


def createShowAudioButtons(audioArray: list):
    keyboard = []
    for audio in audioArray:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=audio.name,
                    callback_data=audioData(id=audio.id, action="sendAudio").pack(),
                )
            ]
        )
    return keyboard


@dp.message(filters.CommandStart())
async def welcome(message: Message):
    createUser(message.from_user.username, message.from_user.id)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="myAudio")]],
        input_field_placeholder="What audio will you upload...",
        resize_keyboard=True,
    )
    answer = useSentences(
        desiredSentence(message.from_user.language_code, ["greeting"]),
        [message.from_user.full_name],
    )
    try:
        await message.answer(answer, reply_markup=keyboard)
    except Exception as e:
        print(f"Error occured: {e}")


@dp.message(filters.Command("help"))
async def help(message: Message):
    answer = desiredSentence(message.from_user.language_code, ["help"])
    try:
        await message.answer(answer)
    except Exception as e:
        print(f"Error occured: {e}")


@dp.message(audioFilter())
async def getAudio(message: Message):
    idContainer = message.voice or message.audio
    audioId = idContainer.file_id
    name = None
    if bool(message.audio):
        name = message.audio.file_name
    buttons = createSetAudioButtons(message.from_user.id)
    audioData = {
        "user": message.from_user.id,
        "name": name or uuid4(),
        "tags": [],
        "timing": [],
        "audioId": audioId,
    }
    caption = f"""
    Name: {audioData['name']}
Tags: {", ".join(audioData["tags"]) or 'None'}
Uses: 0
    """
    isExistedName = createAudioPost(audioData, message.from_user.username)
    if bool(isExistedName):
        await message.answer(f"We already have this {isExistedName}")
        return
    await sendAudioAnswer(
        message, audioId, caption, InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@dp.callback_query(editName.filter(F.action == "edit_name"))
async def nameEdit(query: CallbackQuery,  bot: Bot):
    await bot.send_message(
        text="Enter new name",
        chat_id=query.message.chat.id,
        reply_to_message_id=query.message.message_id,
    )
    createInChangeUser(query, "edit_name")


@dp.callback_query(addTags.filter(F.action == "add_tags"))
async def addTagsQuery(query: CallbackQuery, bot: Bot):
    await bot.send_message(
        text="Add tags\nExample:\nfun, modern, cool",
        chat_id=query.message.chat.id,
        reply_to_message_id=query.message.message_id,
    )
    createInChangeUser(query, "add_tags")


@dp.callback_query(audioData.filter(F.action == "sendAudio"))
async def sendAudio(query: CallbackQuery, callback_data: audioData, bot: Bot):
    audio = Audio.findByid(callback_data.id)
    await bot.send_voice(
        chat_id=query.message.chat.id,
        voice=audio.tgId,
        caption=createCaption(audio),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=createSetAudioButtons(query.message.from_user.id)
        ),
    )


@dp.message(inChangeFilter("edit_name"))
async def audioName(message: Message, userData: inChange):
    del userInChange[str(message.from_user.id)]
    audioData = toggleDb(Audio.updateDataByTgid)(
        id=userData.audioId,
        name=message.text,
        userName=message.from_user.username,
    )
    caption = createCaption(audioData)
    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=userData.messageId,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=createSetAudioButtons(message.from_user.id),
        ),
    )


@dp.message(inChangeFilter("add_tags"))
async def tagAdder(message: Message, userData: inChange):
    del userInChange[str(message.from_user.id)]
    audioData = toggleDb(Audio.updateDataByTgid)(
        id=userData.audioId,
        tags=evaluateTags(message.text),
        userName=message.from_user.username,
    )
    caption = createCaption(audioData)
    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=userData.messageId,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=createSetAudioButtons(message.from_user.id),
        ),
    )


@dp.message(F.text == "myAudio")
async def showAudios(message: Message):
    audios = Audio.getAudioByUsername(message.from_user.username)
    if len(audios) == 0:
        await message.answer("Sry")
        return
    keyboard = createShowAudioButtons(audios)
    await message.answer(
        "Your audios:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@dp.inline_query()
async def showAudio(inline_query: InlineQuery):
    text = inline_query.query or ""
    audioData = Audio.getAudioByName(text)
    if not bool(audioData):
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id="1",
                    title="Sorry",
                    description="We were unable to find this audio",
                    input_message_content=InputTextMessageContent(
                        message_text="We Couldnt find this any results"
                    ),
                )
            ],
            is_personal=True,
            cache_time=5,
        )
        return
    results = []
    for data in audioData:
        results.append(
            InlineQueryResultCachedVoice(
                id=str(data.id), title=data.name, voice_file_id=data.tgId
            )
        )
    await inline_query.answer(
        results=results,
        is_personal=True,
        cache_time=5,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
