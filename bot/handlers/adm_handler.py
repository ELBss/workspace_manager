from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import AdminSG
from keyboards import adm_kbs

router = Router()

@router.message(StateFilter(AdminSG), Command(start))
async def start(message: Message, state: FSMContext):
  await state.clear()
  await message.answer('')
  await state.set_state(AdminSG.choosing_action, reply_markup=adm_kbs.main_kb())

@router.message(AdminSG.choosing_action, F.text == 'Добавить АДМ')
async def add_adm(message: Message, state: FSMContext):
  await message.answer('id')
  await state.set_state(AdminSG.adding_adm)

@router.message(AdminSG.adding_adm, F.text.isnumeric())
async def 


@router.message(AdminSG.choosing_action, F.text == 'Удалить АДМ')
async def del_adm(message: Message, state:FSMContext):
  await message.answer('fdghjkl')
  await state.set_state(AdminSG.deleting_adm)

@router.message(AdminSG.choosing_action, F.text == 'Заблокировать бронирования')
async def del_adm(message: Message, state:FSMContext):
  await message.answer('fdghjkl')
  await state.set_state(AdminSG.block_bookings)

@router.message(AdminSG.choosing_action, F.text == 'Разблокировать бронирования')
async def del_adm(message: Message, state:FSMContext):
  await message.answer('fdghjkl')
  await state.set_state(AdminSG.unblock_bookings)