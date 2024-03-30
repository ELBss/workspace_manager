from datetime import date, timedelta
from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_kb():
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text='book'),
        KeyboardButton(text='list')
    )
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_weekday_kb():
    kb = InlineKeyboardBuilder()

    today = date.today()
    weekdays = [today + timedelta(days=i) for i in range(1, 7)]

    kb.add(InlineKeyboardButton(
        text="Сегодня, " + today.strftime("%d %B"), callback_data=date.isoformat(today)))
    for weekday in weekdays:
        kb.add(InlineKeyboardButton(
            text=weekday.strftime("%d %B"), callback_data=date.isoformat(weekday)))

    return kb.adjust(1, 3, 3).as_markup(resize_keyboard=True)


def get_timeperiod_kb():
    kb = InlineKeyboardBuilder()

    for i in range(1, 5):
        kb.add(InlineKeyboardButton(
            text=f"{15 * i} мин", callback_data=str(15*i)))

    return kb.as_markup(resize_keyboard=True)


# def list_bookings_kb():
#     kb = InlineKeyboardBuilder()

#     return kb.as_markup(resize_keyboard=True)


def registration_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text='nickname again'))

    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
