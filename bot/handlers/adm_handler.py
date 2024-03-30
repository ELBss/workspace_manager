from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states import AdminSG
from keyboards import adm_kbs

router = Router()

# @router.message(AdminSG.choosing_action, F.text.casefold() == 'add/remove adm')
# async def 