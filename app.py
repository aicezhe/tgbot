import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

TOKEN = "8761185657:AAEC8PeqbU34TOUppdpleI-n_nkXi4jeSj8"

BAD_PHRASES = [
    "онлайн заработок",
    "онлайн заработка",
    "ищу людей для дистанционной работы",
    "удаленка",
    "attività lavorativa",
    "тёлка",
    "телка",
    "удалёнка",
    "удаленная работа",
    "удалённая работа",
    "хохол",
    "москаль",
    "Ищу ответственных от 19 лет на полностью удалёнку"
    "Пишите "+" в личные сообщения если интересно"
    "ищу ответственных"
    "на украине"
]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.chat.type == ChatType.PRIVATE, F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Я фильтрую сообщения в группах и удаляю спам-фразы.")


async def is_admin(message: Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ("administrator", "creator")


@dp.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}), F.text)
async def spam_filter(message: Message):
    text = message.text.lower()

    if any(p.lower() in text for p in BAD_PHRASES):

        if await is_admin(message):
            return

        try:
            await message.delete()
            logging.info(f"Deleted message {message.message_id} in chat {message.chat.id}")
        except TelegramForbiddenError:
            logging.error("NO RIGHTS: bot has no permission to delete messages.")
        except TelegramBadRequest as e:
            logging.error(f"BAD REQUEST: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


