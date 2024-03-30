from aiogram.fsm.state import StatesGroup, State


class RegistrationSG(StatesGroup):
    getting_nickname = State()
    waiting_for_code = State()


class AdminSG(StatesGroup):
    choosing_action = State()
    adding_adm = State()



class CommonSG(StatesGroup):
    choosing_action = State()
    choosing_date = State()
    choosing_time = State()
    choosing_period = State()
    booking = State()
