import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

TOKEN = "8761185657:AAGTvI3Sutm_Iejo71AIHo79aLIEstzbLuk"  

BAD_PHRASES = [
    "онлайн заработок",
    "онлайн заработка",
    "ищу людей для дистанционной работы",
    "удаленка",
    "attività lavorativa",
]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.chat.type == ChatType.PRIVATE, F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Я фильтрую сообщения в группах и удаляю спам-фразы.")


@dp.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}), F.text)
async def spam_filter(message: Message):
    text = message.text.lower()

    if any(p.lower() in text for p in BAD_PHRASES):
        try:
            await message.delete() 
            logging.info(f"Deleted message {message.message_id} in chat {message.chat.id}")
        except TelegramForbiddenError:
            logging.error("NO RIGHTS: bot has no permission to delete messages (make it admin + Delete messages).")
        except TelegramBadRequest as e:
            logging.error(f"BAD REQUEST: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())