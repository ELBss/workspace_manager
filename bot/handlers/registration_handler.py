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
    if registered == 'adm':
        await message.answer('uyfg', reply_markup=adm_kbs.adm_main_kb())
        await state.set_state(AdminSG.choosing_action)
    elif registered == 'peer':
        await message.answer('uyfg', reply_markup=common_kbs.main_kb())
        await state.set_state(CommonSG().choosing_action)
    else:
        await message.answer("gimme nickname", reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationSG.getting_nickname)


@router.message(RegistrationSG.getting_nickname, F.text)
async def get_nickname(message: Message, state: FSMContext):
    await registration_requests.send_mail(message.text)
    await message.answer('email sent, gimme code', reply_markup=common_kbs.registration_kb())
    await state.set_state(RegistrationSG.waiting_for_code)


@router.message(RegistrationSG.waiting_for_code, F.text.casefold() == 'nickname again')
async def get_nickname_again(message: Message, state: FSMContext):
    await registration_requests.send_mail(message.text)
    await message.answer('nickname again', reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationSG.getting_nickname)


@router.message(RegistrationSG.waiting_for_code, F.text.isnumeric())
async def try_code(message: Message, state: FSMContext):
    registered = await registration_requests.send_code(message.text)
    if registered:
        await message.answer('registered', reply_markup=common_kbs.main_kb())
        await state.set_state(CommonSG.choosing_action)
    else:
        await message.answer('wrong code, nickname again', reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationSG.getting_nickname)
