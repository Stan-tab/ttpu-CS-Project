from dotenv import load_dotenv
from os import getenv
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import aiogram.filters as filters
from aiogram.types import Message, audio
from components.dictioanary import useSentences
from components.subFunctions import desiredSentence

load_dotenv()
TOKEN = getenv("API_TOKEN")
dp = Dispatcher()


@dp.message(filters.CommandStart())
async def welcome(message: Message):
    answer = useSentences(
        desiredSentence(message.from_user.language_code, ["greeting"]),
        [message.from_user.full_name],
    )
    try:
        await message.answer(answer)
    except Exception as e:
        print(f"Error occured: {e}")


# @dp.message(filters.Command("help"))
# async def help():


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
