import os
from dotenv import load_dotenv
import telebot

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

decidingFromOwnList = False

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "HELPED")

@bot.message_handler(commands=['decide'])
def send_decide(message):
    myListButton = telebot.types.InlineKeyboardButton('My Own List', callback_data='own_list')
    valuesButton = telebot.types.InlineKeyboardButton('New List of things', callback_data='new_list')

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(myListButton)
    keyboard.add(valuesButton)

    bot.send_message(message.chat.id, "Where do you want me to decide from?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'own_list':
        # TODO: Add inline buttons
        pass
    elif call.data == 'new_list':
        bot.send_message(call.message.chat.id, 'Send me the options!')


@bot.message_handler(commands=["view"])
def send_view(message):
    pass

@bot.message_handler(commands=["add"])
def send_view(message):
    pass

@bot.message_handler(commands=["remove"])
def send_view(message):
    pass

bot.polling()