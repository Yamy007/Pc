import sqlite3
import bcrypt


# connect for db
def connect_db():
    global con, cur
    con = sqlite3.connect("User.sqlite")
    cur = con.cursor()
    return cur


def close_db():
    con.close()

# help function
def transformString(value: str):
    mas_value = value.split(",")
    value = ""
    # delete space
    for i in range(len(mas_value)):
        while mas_value[i][0] == " ":
            mas_value[i] = mas_value[i][1:]
    # transform string
    for i in mas_value:
        if i == mas_value[-1]:
            value += "'" + i + "'"
        else:
            value += "'" + i + "'" + ","
    return value


def lastId(table: str):
    try:
        connect_db()
        cur.execute(f"Select id from {table}")
        result = cur.fetchall()
        if result:
            mas_id = []
            for i in result:
                mas_id.append(i)
            close_db()
            return sorted(mas_id)[-1]
        else:
            return list((0,))
    except:
        close_db()
        return list((0,))

def checkName(name: str):
    connect_db()
    try:
        cur.execute(f"Select * from User where name='{name}'")
        result = cur.fetchone()
        close_db()
        if result:
            return False
        else:
            return True
    except:
        close_db()
        return False


def addData(data: str, key: str):
    try:
        temp_db[key] = data
        return True
    except:
        return False


def delData(table: str):
    try:
        connect_db()
        cur.execute(f"DELETE FROM {table}")
        con.commit()
        close_db()
        return True
    except:
        close_db()
        return False

def checkActive(telegram_id:str):
    connect_db()
    try:
        cur.execute(f"Select * from User where telegram_id='{telegram_id}'")
        result = cur.fetchone()
        close_db()
        if result[3] == 'true':
            return True
        else:
            return False
    except:
        close_db()
        return False


# def for db
def all(table: str):
    connect_db()
    try:
        cur.execute(f"SELECT * FROM {table}")
        result = cur.fetchall()
        close_db()
        return result
    except:
        close_db()
        return None


def select(column: str, table: str):
    connect_db()
    try:
        cur.execute(f"Select {column} From {table};")
        result = cur.fetchall()
        close_db()
        return result
    except:
        close_db()
        return None


def delete(table: str, type: str, value: str):
    connect_db()
    try:
        cur.execute(f"DELETE FROM {table} where {type}='{value}'")
        con.commit()
        close_db()
        return True
    except:
        close_db()
        return False


def insert(table: str, value: str):
    connect_db()
    try:
        cur.execute(f"INSERT INTO {table} VALUES({transformString(value)});")
        con.commit()
        close_db()
        return True
    except:
        close_db()
        return False


def find(table: str, type: str, 
         value: str):
    connect_db()
    try:
        cur.execute(f"SELECT * FROM {table} WHERE {type}='{value}'")
        result = cur.fetchall()
        close_db()
        return result
    except:
        close_db()
        return None


def get(table: str, type: str, value: str):
    connect_db()
    try:
        cur.execute(f"SELECT * FROM {table} WHERE {type}='{value}'")
        result = cur.fetchone()
        close_db()
        return result
    except:
        close_db()
        return None


def edit(table: str, type: str, value: str, object: str, id: str):
    connect_db()
    try:
        cur.execute(f"UPDATE {table} SET {type}='{value}' where {object}='{id}'")
        con.commit()
        close_db()
        return True
    except:
        close_db()
        return False



# main


# register
def register(name: str, password: str, telegram_id: str):
    id = lastId("User")[0]+1
    password = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()).decode("utf-8")
    active = 'true'
    ban = 'false'
    if checkName(name):
        try:
            if insert('User', f"{id}, {name}, {password}, {active}, {telegram_id}, {ban}"):
                return True
            else:
                return False
        except:
            return False
    else:
        return False


# login
def login(name: str, password: str, telegram_id: str):

    if name == 'Owners':
        result = get('Owner', 'name', name)
        valid = bcrypt.checkpw(password.encode(), result[2].encode())
        if valid:
            return 'Welcome my love<3'
        else:
            return 'Fuck you, idiot'
    else:
        if checkName(name):
            return 'This name not exist'
        else:
            result = get('User', 'name', name)
            valid = bcrypt.checkpw(password.encode(), result[2].encode())
            if valid:
                edit('User', 'active', 'true', 'telegram_id', telegram_id)
                return 'You login'
            else:
                return 'Bad password'
    
    

# logout
def logout(telegram_id: str):
    checkTelegramId = get('User', 'telegram_id', telegram_id)
    if checkTelegramId:
        if edit('User', 'active', 'false', 'telegram_id', telegram_id):
            return True
        else:
            return False
    else:
        return False


#check_owner 
def check_owner(telegram_id: str):
    result = get('Owner', 'telegram_id', telegram_id)
    if result:
        edit('Owner', 'active', 'true', telegram_id, telegram_id)
        return True
    else:
        return False
    

#owner_login
def owner_login(name: str, password: str):
    result = get('Owner', 'name', name)
    if result:
        edit('Owner', 'active', 'true', 'name', name)
        valid = bcrypt.checkpw(password.encode(), result[2].encode())
        if valid:
            return True
        else:
            return False

#owner_logout
def owner_logout(telegram_id: str):
    result = get('Owner', 'telegram_id', telegram_id)
    if result:
        edit('Owner', 'active', 'false', 'name', name)
        

# control user
def allInfo(table: str):
    connect_db()
    try:
        result = select('name, telegram_id, ban', table)
        close_db()
        return result
    except:
        close_db()
        return None
    
def IdByName(name: str):
    connect_db()
    try:
        result =  cur.execute(f"SELECT telegram_id FROM User WHERE name = '{name}'")
        result = cur.fetchone()
        close_db()
        return result[0]
    except:
        close_db()
        return None
    




def allUser():
    result = all('User')
    if result:
        return result
    else:
        return False
    

def banUser(telegram_id: str):
    result = get('User', 'telegram_id', telegram_id)
    if result:
        if result[5] == 'false':
            if edit('User', 'ban', 'true', 'telegram_id', telegram_id):
                return True
            else:
                return False
    else:
        return False
    
    
def unBanUser(telegram_id: str):
    result = get('User', 'telegram_id', telegram_id)
    if result:
        if result[5] == 'true':
            if edit('User', 'ban', 'false', 'telegram_id', telegram_id):
                return True
            else:
                return False
    else:
        return False
    
    
def banAll(telegram_id: str):
    if get('Owner','telegram_id', telegram_id):
        connect_db()
        try:
            cur.execute(f"UPDATE User SET ban ='true' where ban ='false'")
            con.commit()
            close_db()
            return True
        except:
            close_db()
            return False    
    else:
        print('You are not owner')   





print(banAll(10492695911))
# role for user


# bot main

# config bot
