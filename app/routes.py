from app import app, db  # bot,
from app.models import Post, VkPublic, Task
from apscheduler.schedulers.background import BackgroundScheduler
# import requests
# import re
# from bs4 import BeautifulSoup
# import json
# import telegram
from datetime import datetime
from app.parcer import VK_public, Api, Post as PostClass
from app.bot_sender import TelegramSend
import json


# start admin
from app import admin_bot


def send_process():
    unsend_posts = Task.query.filter_by(send=0).all()
    if unsend_posts:
        # task_post = unsend_posts[0]
        used_tokens = []
        for task_post in unsend_posts:
            if task_post.bot_token not in used_tokens:
                internal_post = Post.query\
                                    .filter_by(internal_id=task_post.post_id)\
                                    .first()
                parsed_json = json.loads(internal_post.data_json)
                # print(parsed_json)
                internal_post = PostClass(parsed_json, from_db=True)
                success = False
                while not success:
                    try:
                        print('start sending')
                        # print(internal_post.audio)
                        tg_api = TelegramSend(task_post.bot_token,
                                              task_post.tg_channel)
                        tg_api.send([internal_post])
                        success = True
                        task_post.send = 1
                        db.session.commit()
                    except Exception as e:
                        print(e)
                used_tokens.append(task_post.bot_token)


def make_things_with_public(vk_pub):

    api = Api('85b94daf85b94daf85b94daf2e85c8262e885b985b94dafdb1c75e53197a87568527221')

    pub = VK_public(vk_pub)

    extracted_posts = pub.download_last_posts(api)
    new_posts = pub.save_unsaved_post(extracted_posts)
    pub.send_new_posts(new_posts)


def main_func():

    vk_publics = VkPublic.query.all()

    if len(vk_publics) > 1:

        # if 'collection9' not in [x.address for x in vk_publics]:
        #     d = VkPublic(address='collection9',
        #                  bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
        #                  tg_channel='@novostibyte')
        #     db.session.add(d)
        #     db.session.commit()
        #     make_things_with_public(d)

        for vk_public in vk_publics:
            make_things_with_public(vk_public)
    else:
        pass
        # a = VkPublic(address='overhear',
        #              bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
        #              tg_channel='@vk_podslushano')
        # b = VkPublic(address='mayland',
        #              bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
        #              tg_channel='@vk_mayland')
        # c = VkPublic(address='yebenya',
        #              bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
        #              tg_channel='@vk_estetika_ebeney')
        # db.session.add(c)
        # db.session.add(b)
        # db.session.add(a)
        # db.session.commit()
        # make_things_with_public(c)
        # make_things_with_public(b)
        # make_things_with_public(a)


@app.route('/healthcheck', methods=['GET', 'POST'])
def healthcheck():
    # print('Healthcheck is start...')
    # data = SaveData.query.first()
    # data = json.loads(data.data)
    # print(f'Database content: {data}')
    # # main_func()
    return 'Health check completed successful.'


@app.route('/', methods=['GET', 'POST'])
def test():
    # print('Test is start...')
    # data = SaveData.query.first()
    # data = json.loads(data.data)
    # print(f'Database content: {data}')
    # main_func()
    return 'Test completed successful.'


# main_func()
def test_scheduler():
    print('Test scheduler is starting...')
    main_func()


p = Task.query.filter_by(tg_channel='@novostibyte').all()

for pp in p:
    Post.query\
        .filter_by(internal_id=pp.post_id)\
        .delete()
Task.query.filter_by(tg_channel='@novostibyte').delete()
VkPublic.query.filter_by(address='collection9').delete()
db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(test_scheduler, 'interval', seconds=300,
                  next_run_time=datetime.now())
scheduler.add_job(send_process, 'interval', seconds=35)
scheduler.start()
