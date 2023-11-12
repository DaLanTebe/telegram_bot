import telebot
from telebot import types

bot = telebot.TeleBot('6568553523:AAH7TXWLR_Iy4_O4yQn0-ZI5CpeE_A_5zl4')

name = ''
surname = ''
age = 0


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чо надо?")
        bot.register_next_step_handler(message, start)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, кожаный")


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, 'Как тебя зовут?')
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    name = message.text
    bot.send_message(message.from_user.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Да", callback_data="yes"))
    keyboard.add(types.InlineKeyboardButton(text="Нет", callback_data="no"))
    bot.send_message(message.from_user.id, 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call:True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню :')
    elif call.data == "no":
        callback_worker(call)


bot.polling(none_stop=True, interval=0)
