from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import filters, Text
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, WebAppInfo, KeyboardButtonPollType, \
    InlineKeyboardButton, ReplyKeyboardRemove
    
import sqlite3
import bcrypt
    
from config import TOKEN, Reg

from core import *

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if checkActive(message.chat.id):
        await message.answer('Hi my love')
    else:
        checkTelegramId = get('User', 'telegram_id', message.chat.id)
        if checkTelegramId:
            if checkTelegramId[3] == 'true':
                init_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                logout = types.KeyboardButton('/logout')
                go_to_function = types.KeyboardButton('/go')
                init_keyboard.add(logout)
                init_keyboard.add(go_to_function)
                await message.answer('Choose action', reply_markup=init_keyboard)
            else:
                init_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
                login = types.KeyboardButton('/login')
                init_button.add(login)
                await message.answer('You must login', reply_markup=init_button)
        else:
            register = types.KeyboardButton('/register')
            init_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
            init_button.add(register)
            await message.answer("Hi, I glad to see you", reply_markup=init_button)


    
@dp.message_handler(commands=['register'])
async def register_bot(message: types.Message):
    if checkActive(message.chat.id):
        await message.answer('You have already registered')
    else:
        await message.answer("Enter your name")
        await Reg.name.set()


@dp.message_handler(state=Reg.name)
async def register_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Enter your password")
    await Reg.password.set()
    
    
@dp.message_handler(state=Reg.password)
async def register_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    init_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    logout = types.KeyboardButton('/logout')
    go_to_function = types.KeyboardButton('/go')
    init_keyboard.add(logout)
    init_keyboard.add(go_to_function)
    if not get('User', 'telegram_id', message.chat.id):
        if register(data['name'], data['password'], message.chat.id):
            await message.answer('Choose action', reply_markup=init_keyboard)       
        else:
            await message.answer('This name is busy')
    else:
        await message.answer('You have already registered', reply_markup=init_keyboard)        
    await state.finish()
    
@dp.message_handler(commands=['logout'])
async def complete(message: types.Message):
    if logout(message.chat.id):
        init_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
        login = types.KeyboardButton('/login')
        init_button.add(login)
        await message.answer('You logout', reply_markup=init_button)
    else:
        await message.answer('You have already logout')    
        
@dp.message_handler(commands=['login'])
async def login_bot(message: types.Message):
    if checkActive(message.chat.id):
        await message.answer('You have already login')
    else:
        await message.answer("Enter your name")
        await Reg.name_login.set()
        
@dp.message_handler(state=Reg.name_login)
async def login_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_login'] = message.text
    await message.answer("Enter your password")
    await Reg.password_login.set()

@dp.message_handler(state=Reg.password_login)
async def login_password(message: types.Message, state: FSMContext):
    init_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    logout = types.KeyboardButton('/logout')
    go = types.KeyboardButton('/go')
    init_keyboard.add(go)
    init_keyboard.add(logout)
    
    async with state.proxy() as data:
        data['password_login'] = message.text

    await message.answer(login(data['name_login'], data['password_login'], message.chat.id), reply_markup=init_keyboard)
    await state.finish()
            
@dp.message_handler(commands=['owner'])
async def owner(message: types.Message):
    if check_owner(message.chat.id):
        _init_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        allUsers = types.KeyboardButton('/allUsers')
        banUser = types.KeyboardButton('/banUser')
        roleUser = types.KeyboardButton('/roleUser')
        banAll = types.KeyboardButton('/banAll')
        _init_keyboard.add(allUsers)
        _init_keyboard.add(banUser)
        _init_keyboard.add(roleUser)
        _init_keyboard.add(banAll)
        
        await message.answer('Hi yamy', reply_markup=_init_keyboard)#its my telegram id
    else:
        await message.answer('You must login')

@dp.message_handler(commands=['ownerLogin'])
async def ownerLogin(message: types.Message):
    if check_owner(message.chat.id):
        await message.answer('You have already login')
    else:
        await message.answer("Enter your name")
        await Reg.owner_name_login.set()
    
@dp.message_handler(state=Reg.owner_name_login)
async def owner_login_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['owner_name_login'] = message.text
    await message.answer("Enter your password")
    await Reg.owner_password_login.set()
    
@dp.message_handler(state=Reg.owner_password_login)
async def owner_login_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['owner_password_login'] = message.text
    if owner_login(data['owner_name_login'], data['owner_password_login']):
        await message.answer('Hi yamy')
    else:
        await message.answer('You must login as owner')

@dp.message_handler(commands=['allUsers'])
async def allUsers(message: types.Message):


if __name__ == '__main__':
    executor.start_polling(dp)