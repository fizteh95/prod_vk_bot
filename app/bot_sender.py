# import asyncio

# from aiogram import Bot, Dispatcher, types
# from aiogram.utils import executor

import telebot
from time import sleep
from telebot import types
# import telegram
# from telebot import apihelper


class TelegramSend:

    def __init__(self, bot_token, tg_channel):
        self.API_TOKEN = bot_token
        # PROXY_URL = 'http://46.4.96.87:80'
        # apihelper.proxy = {'http': PROXY_URL, 
        #                    # 'https': 'socks5://195.201.137.246:1080'
        #                    }
        # self.bot = Bot(token=self.API_TOKEN, proxy=PROXY_URL)
        self.bot = telebot.TeleBot(self.API_TOKEN)
        # , parse_mode=types.ParseMode.HTML
        # self.dp = Dispatcher(self.bot)
        self.tg_channel = tg_channel

    def broadcaster(self, posts: list) -> int:
        """

        """
        for post in posts:
            if (not post.photo) and post.text:
                self.bot.send_message(self.tg_channel, post.text)
                sleep(.05)

            if (len(post.photo) > 1) and (len(post.photo) < 10):

                medias = []

                if post.text:
                    medias.append(types.InputMediaPhoto(post.photo[0], post.text))
                else:
                    medias.append(types.InputMediaPhoto(post.photo[0]))

                for i in range(1, len(post.photo)):
                    medias.append(types.InputMediaPhoto(post.photo[i]))

                try:
                    self.bot.send_media_group(self.tg_channel, medias)
                except Exception as e:
                    print(e)
                sleep(.05)  # 20 messages per second
                # bot = telegram.Bot(token=self.API_TOKEN)
                # media = []


                # if post.text:
                #     media.append(dict(type='photo', media=post.photo[0], caption=post.text))
                # else:
                #     media.append(dict(type='photo', media=post.photo[0]))

                # for i in range(1, len(post.photo)):
                #     media.append(dict(type='photo', media=post.photo[i]))


                # bot_message = bot.sendMediaGroup(self.tg_channel, media)
                sleep(.05)
                # sleep(5)
                # print('one sleep')
                # sleep(5)
                # print('two sleep')
                # sleep(5)
                # print('three sleep')
                # sleep(5)
                # print('four sleep')
                # sleep(5)
                # print('five sleep')

            if len(post.photo) == 1:
                if post.text:
                    self.bot.send_photo(self.tg_channel, post.photo[0],
                                        caption=post.text)
                else:
                    self.bot.send_photo(self.tg_channel, post.photo[0])
                sleep(.05)

            if post.audio:
                for audio in post.audio:
                    self.bot.send_audio(self.tg_channel, audio)
                    sleep(.05)

        return True

    def send(self, posts):  # , bot_token, tg_channel
        # executor.start(self.dp, self.broadcaster(posts))
        self.broadcaster(posts)
