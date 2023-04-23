import os
from dotenv import load_dotenv
import telebot

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "HELPED")

@bot.message_handler(commands=['decide'])
def send_decide(message):
    foodListButton = telebot.types.InlineKeyboardButton('Food List', callback_data='food_list')
    activityListButton = telebot.types.InlineKeyboardButton('Activity List', callback_data='activity_list')
    newListButton = telebot.types.InlineKeyboardButton('New List of things', callback_data='new_list')

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(foodListButton)
    keyboard.add(activityListButton)
    keyboard.add(newListButton)

    bot.send_message(message.chat.id, "Where do you want me to decide from?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'food_list':
        pass
    elif call.data == 'activity_list':
        pass
    elif call.data == 'new_list':
        msg = bot.send_message(call.message.chat.id, 'Send me the options! (Separated by spaces)')
        bot.register_next_step_handler(msg, process_new_list)

def process_new_list(message):
    print("Hello")
    print(message.text)


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