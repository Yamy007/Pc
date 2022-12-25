import telebot, wikipedia, re,alsaaudio, time
from screen_brightness_control import get_brightness, set_brightness
from telebot import types
import os,pyautogui
import subprocess

    

API_TOKEN = '5474894861:AAHMzbMV62rkCT05xR_VHzRfAnVc9DWu3zY'

bot = telebot.TeleBot(API_TOKEN)

def vol(message):
   mix = alsaaudio.Mixer()
   vol = mix.getvolume()
   try:
      parse = int(message)
      if parse < 0:
         mix.setvolume(0)
      elif parse > 100:
         mix.setvolume(100)
      else:
         mix.setvolume(int(message)) 
   except:
      return 'Fuck you, stupid idiot!'

def getBrightness():
    return get_brightness()[0]


def bright(message):
    try:
       parse = int(message)
       if parse < 0:
          set_bright(0)
       elif parse > 100:
          set_bright(100)
       else:
          set_brightness(int(message))
    except:
       return 'Fuck you, stupid idiot!'


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext=ny.content[:1000]
        wikimas=wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception as e:
        return 'Not Found 404'


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Search(EN)")
    item2=types.KeyboardButton("Search(UKR)")
    item3=types.KeyboardButton("Reboot")
    item4=types.KeyboardButton("ShutDown")
    item5=types.KeyboardButton("Block")
    item6=types.KeyboardButton("UnBlock")
    item7=types.KeyboardButton("Suspend")        
    item8=types.KeyboardButton("Volume")
    item9=types.KeyboardButton("Bright")
    item10=types.KeyboardButton("BlockKeyboard") 
    item11=types.KeyboardButton("UnBlockKeyboard")
   #  item12=types.KeyboardButton("Bluetooth")    !TODO
    

    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    markup.add(item6)
    markup.add(item7)
    markup.add(item8)
    markup.add(item9)
    markup.add(item10)
    markup.add(item11)
   #  markup.add(item12) 
    bot.send_message(m.chat.id, 'On duty, fuck you',  reply_markup=markup)




@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Search(EN)':
       wikipedia.set_lang("en")
       bot.send_message(message.chat.id, "Enter word for search:")
       bot.register_next_step_handler(message, search_wiki)
    elif message.text.strip() == 'Search(UKR)':
       wikipedia.set_lang("uk")
       bot.send_message(message.chat.id, "Ведіть слово для пошуку:")
       bot.register_next_step_handler(message, search_wiki)
    elif message.text.strip() == 'Reboot':
       os.system("reboot") 
       bot.send_message(message.chat.id, "Complete")
    elif message.text.strip() == "ShutDown":
       os.system("shutdown now") 
       bot.send_message(message.chat.id, "Complete")
    elif message.text.strip() == 'Block':
       os.system("loginctl lock-session") 
       bot.send_message(message.chat.id, "Complete")
    elif message.text.strip() == 'UnBlock':
       os.system("loginctl unlock-session") 
       bot.send_message(message.chat.id, "Complete")
    elif message.text.strip() == 'Suspend':
       os.system("systemctl suspend") 
       bot.send_message(message.chat.id, "Complete") 
    elif message.text.strip() == 'Volume':
       bot.send_message(message.chat.id, "Enter new value volume")
       bot.register_next_step_handler(message, set_volume) 
    elif message.text.strip() == 'Bright':
       bot.send_message(message.chat.id, "Enter new value Bright")
       bot.register_next_step_handler(message, set_bright)
    elif message.text.strip() == 'BlockKeyboard':
       bot.send_message(message.chat.id, "Complete") 
       os.system('bash -c "sleep 1 && xtrlock"')

    elif message.text.strip() == 'UnBlockKeyboard':
       pyautogui.press("2")
       pyautogui.press("8")
       pyautogui.press("0")
       pyautogui.press("3")
       pyautogui.press("enter")
       bot.send_message(message.chat.id, "Complete") 
   #  elif message.text.strip() == 'Bluetooth':
   #     f=os.popen('bluetoothctl')
      
   #     rd=f.read()
   #     time.sleep(5)
   #     os.system('exit')
   #     bot.send_message(message.chat.id, rd) 
   #     f.close()


@bot.message_handler(content_types=["text"])
def search_wiki(message):
    bot.send_message(message.chat.id, getwiki(message.text))        


@bot.message_handler(content_types=["text"])
def set_volume(message):
    bot.send_message(message.chat.id, vol(message.text))        


@bot.message_handler(content_types=["text"])
def set_bright(message):
    bot.send_message(message.chat.id, bright(message.text))     


 
bot.polling(none_stop=True, interval=0)
