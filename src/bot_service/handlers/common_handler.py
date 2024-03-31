from datetime import datetime, timedelta, date

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import CommonSG
from keyboards import common_kbs
from db_requests import booking_requests


router = Router()


@router.message(StateFilter(CommonSG), Command('start'))
async def start(message: Message, state: FSMContext):
    state.clear()
    await state.update_data(user_id=message.from_user.id)
    await message.answer("Выбери действие:", reply_markup=common_kbs.main_kb())
    await state.set_state(CommonSG.choosing_action)


@router.message(CommonSG.choosing_action, F.text == 'Забронировать')
async def book(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await message.answer("Дата бронирования:", reply_markup=common_kbs.get_weekday_kb())
    await state.set_state(CommonSG.choosing_date)


@router.callback_query(CommonSG.choosing_date)
async def get_date(callback: CallbackQuery, state: FSMContext):
    await state.update_data(date=callback.data)
    await callback.answer('Выбрана дата: ' + callback.data)
    await callback.message.edit_text('Время начала бронирования (в формате чч:мм):')
    await state.set_state(CommonSG.choosing_time)


@router.message(CommonSG.choosing_time, F.text.regexp(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]'))
async def choose_time(message: Message, state: FSMContext):
    data = await state.get_data()
    begin = data['date'] + 'T' + message.text + ':00'
    await state.update_data(begin=begin)
    await message.answer('Выбранное время: ' + data['date'] + ' ' + message.text)
    await message.answer("Период бронирования: ", reply_markup=common_kbs.get_timeperiod_kb())
    await state.set_state(CommonSG.choosing_period)


@router.message(CommonSG.choosing_time)
async def invalid_time(message: Message):
    await message.answer("Неправильный формат времени, введите снова")


@router.callback_query(CommonSG.choosing_period)
async def get_period(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    end = datetime.strptime(
        data['begin'], '%Y-%m-%dT%H:%M:%S') + timedelta(minutes=int(callback.data))

    await state.update_data(end=datetime.strftime(end, '%Y-%m-%dT%H:%M:%S'))

    data = await state.get_data()
    booked = await booking_requests.book(data)
    # booked = True
    if booked:
        await callback.answer('Забронировано')
        await callback.message.edit_text('Забронировано!')
    else:
        await callback.answer('Не забронировано')
        await callback.message.edit_text('На это время свободных переговорок нет')
    await state.clear()
    await state.set_state(CommonSG.choosing_action)


@router.message(CommonSG.choosing_action, F.text == 'Отменить бронирование')
async def list(message: Message, state: FSMContext):
    await message.answer("your bookings", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CommonSG.choosing_time)
