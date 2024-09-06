from aiogram.filters.command import Command
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from callbacks_classes import NewScoreCallback
from aiogram import Dispatcher
import utils

dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder()
    # Добавляем в сборщик одну кнопку
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text='Посмотреть статистику'))
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

from aiogram import F

# Хэндлер на команды /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='Да', callback_data=NewScoreCallback(new_score='True').pack()))
    builder.add(types.InlineKeyboardButton(text='Нет', callback_data=NewScoreCallback(new_score='False').pack()))
    await message.answer("Сохранить результат в базу данных?", reply_markup=builder.as_markup(resize_keyboard=True))
    builder.adjust(1)

@dp.message(F.text=="Посмотреть статистику")
@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    stats = await utils.get_stats()
    answer = ''
    for user_id, score in stats.items():
        answer += f'User_id: {user_id},\t score: {score}\n'
    await message.answer(answer)