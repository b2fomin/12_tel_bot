from aiogram.filters.callback_data import CallbackData

class AnswerCallback(CallbackData, prefix='ans_call'):
    answer_index: int
    new_score: bool


class NewScoreCallback(CallbackData, prefix='new_score'):
    new_score: bool
