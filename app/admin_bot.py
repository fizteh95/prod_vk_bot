# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler.
"""

import telebot
from telebot import types
from app import app, db
from flask import request
from app.models import VkPublic, User


API_TOKEN = '873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}
print('starting admin...')

# class User:
#     def __init__(self, name):
#         self.name = name
#         self.age = None
#         self.sex = None


# cid = m.chat.id


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])  # 'help', 
def send_welcome(message):
    cid = message.chat.id
    users = User.query.filter_by(chat_id=cid).all()
    if not users:
        u = User(chat_id=cid)
        db.session.add(u)
        db.session.commit()
    user_dict[cid] = {}
    msg = bot.send_message(cid, '''Привет, этот бот репостит посты из пабликов ВК в каналы Телеграма. Чтобы это сделать, тебе надо будет создать бота через @BotFather, прислать сюда токен созданного бота, а также ссылку на паблик ВК. Для начала создай бота, и пришли в этот чат токен нового бота.''')
#     msg = bot.reply_to(message, """\
# Hi there, I am Example bot.
# What's your name?
# """)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        cid = message.chat.id
        if ':' in message.text:
            # user = User.query.filter_by(chat_id=cid).first()
            user_dict[cid]['token'] = message.text
            msg = bot.send_message(cid, '''Отлично! Теперь создай канал в Телеграме и пришли его адрес в формате @channel''')
            bot.register_next_step_handler(msg, process_age_step)
        else:
            msg = bot.send_message(cid, '''Кажется, это не токен. Попробуй еще раз.''')
            bot.register_next_step_handler(msg, process_name_step)
            return
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        cid = message.chat.id
        if '@' in message.text:
            user_dict[cid]['tg_channel'] = message.text
            msg = bot.send_message(cid, '''Хорошо. Теперь пришли мне ссылку на паблик ВК в формате https://vk.com/artelec''')
            bot.register_next_step_handler(msg, process_sex_step)
        else:
            msg = bot.send_message(cid, '''Кажется, это не валидный адрес. Попробуй еще раз.''')
            bot.register_next_step_handler(msg, process_age_step)
            return
    except Exception as e:
        bot.reply_to(message, 'oooops')
    # try:
    #     chat_id = message.chat.id
    #     age = message.text
    #     if not age.isdigit():
    #         msg = bot.reply_to(message, 'Age should be a number. How old are you?')
    #         bot.register_next_step_handler(msg, process_age_step)
    #         return
    #     user = user_dict[chat_id]
    #     user.age = age
    #     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    #     markup.add('Male', 'Female')
    #     msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
    #     bot.register_next_step_handler(msg, process_sex_step)
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        cid = message.chat.id
        if '://vk.com/' in message.text:
            user_dict[cid]['vk_pub'] = message.text.split('/')[-1]

            user = User.query.filter_by(chat_id=cid).first()
            new_pub = VkPublic(address=user_dict[cid]['vk_pub'],
                               bot_token=user_dict[cid]['token'],
                               tg_channel=user_dict[cid]['tg_channel'],
                               user_id=user.id)
            db.session.add(new_pub)
            db.session.commit()

            msg = bot.send_message(cid, '''Мы закончили! Через несколько минут сообщения начнут приходить в канал Телеграма. Спасибо что воспользовался нашим сервисом ;)''')
        else:
            msg = bot.send_message(cid, '''Кажется, это не валидный адрес. Попробуй еще раз.''')
            bot.register_next_step_handler(msg, process_sex_step)
            return

    except Exception as e:
        bot.reply_to(message, 'oooops')
    # try:
    #     chat_id = message.chat.id
    #     sex = message.text
    #     user = user_dict[chat_id]
    #     if (sex == u'Male') or (sex == u'Female'):
    #         user.sex = sex
    #     else:
    #         raise Exception()
    #     bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
    # except Exception as e:
    #     bot.reply_to(message, 'oooops')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

# bot.polling()

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/set_webhook")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://flask-svalkobot.herokuapp.com/' + API_TOKEN)
    return "!", 200
