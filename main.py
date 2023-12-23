from dotenv import load_dotenv, find_dotenv
import telebot
import os 
from telebot import types
import random

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_hello(message):
    bot.send_message(message.chat.id, "Hello!👋")

questions = {
    "5 X 6 = ?":"30",
    "12 + 5 = ?":"17",
    "12 - 5 = ?":"7",
    "10 + 3 = ?":"13",
    "115 / 5 = ?":"23"  
}

def make_question(question):
    global questions
    markup = types.InlineKeyboardMarkup(row_width=3)
    a = types.InlineKeyboardButton(questions[question], callback_data='True')
    b = types.InlineKeyboardButton(random.randint(1, 100), callback_data='False')
    c = types.InlineKeyboardButton(random.randint(1, 100), callback_data='False')
    markup.add(a, b, c)
    return markup

@bot.message_handler(commands=['quiz'])
def math_test(message):
    global questions
    count = 0
    for question in questions.keys():
        markup = make_question(question)
        bot.send_message(message.chat.id, question, reply_markup=markup)
        @bot.callback_query_handler(func=lambda call: True)
        def handle_query(call):
            if call.data == 'True':
                bot.send_message(call.message.chat.id, 'Correct! ✅')
            else:
                bot.send_message(call.message.chat.id, 'The answer is wrong! ❌')
                bot.send_message(message.chat.id, question, reply_markup=markup)
    count += 1

bot.infinity_polling()