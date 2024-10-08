import asyncio
import logging
from aiogram import Bot
from callbacks import *
from buttons import dp
from database import create_table

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '7078851959:AAH6aahc7xDC581Ozje15QOK1nU9VW1Tn-k'


# Объект бота
bot = Bot(token=API_TOKEN)

# Запуск процесса поллинга новых апдейтов
async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())