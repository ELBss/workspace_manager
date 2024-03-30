from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb():
    kb = ReplyKeyboardBuilder()

    kb.row(
        KeyboardButton(text='Добавить АДМ'),
        KeyboardButton(text='Удалить АДМ')
    )
    kb.row(
        KeyboardButton(text='Заблокировать бронирования'),
        KeyboardButton(text='Разблокировать бронирования')
    )
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def 
