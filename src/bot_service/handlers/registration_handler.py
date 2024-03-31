from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import RegistrationSG, AdminSG, CommonSG
from keyboards import common_kbs, adm_kbs
from db_requests import registration_requests


router = Router()


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    registered = await registration_requests.check_id(message.from_user.id)
    # registered = 'peer'
    if registered == 'ADM':
        await message.answer('uyfg', reply_markup=adm_kbs.adm_main_kb())
        await state.set_state(AdminSG.choosing_action)
    elif registered == 'COMMON':
        await message.answer('Выбери действие:', reply_markup=common_kbs.main_kb())
        await state.set_state(CommonSG().choosing_action)
    else:
        await message.answer("Введи свой ник на платформе", reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationSG.getting_nickname)


@router.message(RegistrationSG.getting_nickname, F.text)
async def get_nickname(message: Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await registration_requests.send_mail(message.text)
    await message.answer('Введи код, отправленный на почту', reply_markup=common_kbs.registration_kb())
    await state.set_state(RegistrationSG.waiting_for_code)


@router.message(RegistrationSG.waiting_for_code, F.text == 'Ввести ник заново')
async def get_nickname_again(message: Message, state: FSMContext):
    await registration_requests.send_mail(message.text)
    await message.answer('Введи ник', reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationSG.getting_nickname)


@router.message(RegistrationSG.waiting_for_code, F.text)
async def try_code(message: Message, state: FSMContext):
    data = await state.get_data()
    registered = await registration_requests.send_code(data['nickname'], message.text, message.from_user.id)
    # registered = True
    if registered:
        await message.answer('Пользователь зарегистрирован', reply_markup=common_kbs.main_kb())
        await state.set_state(CommonSG.choosing_action)
    else:
        await message.answer('Неверный код, введи ник снова', reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationSG.getting_nickname)
