import database as db
from quiz_data import quiz_data
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from callbacks_classes import AnswerCallback

async def new_quiz(user_id, message, new_score=True):
    # получаем id пользователя, отправившего сообщение
    # сбрасываем значение текущего индекса вопроса квиза в 0
    current_question_index = 0
    if new_score:
        await db.update_score(user_id, 0)
    await db.update_quiz_index(user_id, current_question_index)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id, new_score)

async def get_question(message, user_id, new_score):

    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await db.get_quiz_index(user_id)
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts, new_score)
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

def generate_options_keyboard(answer_options, new_score):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()

    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for i, option in enumerate(answer_options):
        builder.add(types.InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            callback_data=AnswerCallback(new_score=new_score, answer_index=i).pack())
        )

    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()

async def get_stats():
    return await db.get_stats()