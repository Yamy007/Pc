from core import *



def createOwner():
    delData('Owner')
    name = input('Enter your name: ')
    password = input('Enter your password: ')
    telegram_id = input('Enter your telegram_id: ')
    active = 'false'
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")
    if insert('Owner', f"1, {name}, {password}, {telegram_id}, {active}"):
        print('Success')
    else:
        print('Error')

createOwner()