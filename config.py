from aiogram.dispatcher.filters.state import StatesGroup, State

TOKEN = '5474894861:AAHMzbMV62rkCT05xR_VHzRfAnVc9DWu3zY'

class Reg(StatesGroup):
    name = State()
    password = State()
    telegram_id = State()
    name_login = State()
    password_login = State()
    owner_password_login = State()
    owner_name_login = State()


