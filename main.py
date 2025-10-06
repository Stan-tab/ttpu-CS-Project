from dotenv import load_dotenv
from os import getenv
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import aiogram.filters as filters
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
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


def createButtons(userId):
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
        [
            InlineKeyboardButton(
                text="Change timing",
                callback_data=SetTimings(
                    userId=userId,
                    action="timing",
                ).pack(),
            )
        ],
    ]


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
    buttons = createButtons(message.from_user.id)
    audioData = {
        "user": message.from_user.id,
        "name": uuid4(),
        "tags": [],
        "timing": [],
        "audioId": audioId,
    }
    caption = f"""
    Name: {audioData['name']}
Tags: {", ".join(audioData["tags"]) or 'None'}
Uses: 0
    """
    await sendAudioAnswer(
        message, audioId, caption, InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    createAudioPost(audioData, message.from_user.username)


@dp.callback_query(editName.filter(F.action == "edit_name"))
async def nameEdit(query, callback_data, bot):
    idContainer = query.message.voice or query.message.audio
    audioId = idContainer.file_id
    await bot.send_message(
        text="Enter new name",
        chat_id=callback_data.userId,
        reply_to_message_id=query.message.message_id,
    )
    userInChange[str(callback_data.userId)] = inChange(
        query.message.message_id, audioId
    )


@dp.message(inChangeFilter())
async def audioName(message, userData):
    del userInChange[str(message.from_user.id)]
    audioData = updateAudioName(message.text, userData)
    caption = f"""
    Name: {audioData.name}
Tags: {", ".join(audioData.tags)}
Uses: {audioData.uses}
"""
    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=userData.messageId,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=createButtons(message.from_user.id)),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
