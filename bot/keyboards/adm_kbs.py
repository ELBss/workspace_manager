from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def adm_main_kb():
    kb = ReplyKeyboardBuilder()

    kb.row(
        KeyboardButton(text='add/remove adm'),
        KeyboardButton(text='rooms management')
    )
    return kb.as_markup(resize_keyboard=True, )



