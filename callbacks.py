from buttons import dp
from aiogram import types
from quiz_data import quiz_data
import database as db
import utils
from utils import AnswerCallback

@dp.callback_query(AnswerCallback.filter())
async def quiz_answer(callback: types.CallbackQuery):
    data = callback.data
    data_idx = int(data.split(':')[1])

    # Получение текущего вопроса для данного пользователя
    current_question_index = await db.get_quiz_index(callback.from_user.id)
    user_answer = quiz_data[current_question_index]['options'][data_idx]
    right_answer_idx = quiz_data[current_question_index]['correct_option']
    right_answer = quiz_data[current_question_index]['options'][right_answer_idx]
    if user_answer == right_answer:
        await db.update_score(callback.from_user.id, db.get_score(callback.from_user.id) + 1)
        await callback.message.answer(f'Ваш ответ {user_answer} верен!')
    else:
        await callback.message.answer(f'Ваш ответ {user_answer} неверен!\n Правильный ответ: {right_answer}')

    await callback.bot.delete_message(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id)

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await db.update_quiz_index(callback.from_user.id, current_question_index)

    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await utils.get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")