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


def send_process():
    unsend_posts = Task.query.filter_by(send=0).all()
    if unsend_posts:
        task_post = unsend_posts[0]
        internal_post = Post.query.filter_by(id=task_post.post_id).first()
        internal_post = PostClass(internal_post.data_json)
        success = False
        while not success:
            try:
                print('start sending')
                tg_api = TelegramSend(task_post.bot_token,
                                      task_post.tg_channel)
                tg_api.send([internal_post])
                success = True
                task_post.send = 1
                db.session.commit()
            except Exception as e:
                print(e)


def make_things_with_public(vk_pub):

    api = Api('85b94daf85b94daf85b94daf2e85c8262e885b985b94dafdb1c75e53197a87568527221')

    pub = VK_public(vk_pub)

    extracted_posts = pub.download_last_posts(api)
    new_posts = pub.save_unsaved_post(extracted_posts)
    pub.send_new_posts(new_posts)


def main_func():
    vk_publics = VkPublic.query.all()
    if len(vk_publics) > 1:
        for vk_public in vk_publics:
            make_things_with_public(vk_public)
    elif len(vk_publics) == 1:
        b = VkPublic(address='mayland',
                     bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
                     tg_channel='@vk_podslushano')
        db.session.add(b)
        db.session.commit()
        vk_publics = VkPublic.query.all()
        for vk_public in vk_publics:
            make_things_with_public(vk_public)
    else:
        a = VkPublic(address='overhear',
                     bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
                     tg_channel='@vk_podslushano')
        b = VkPublic(address='mayland',
                     bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
                     tg_channel='@vk_podslushano')
        db.session.add(b)
        db.session.add(a)
        db.session.commit()
        make_things_with_public(a)
        make_things_with_public(b)


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


scheduler = BackgroundScheduler()
scheduler.add_job(test_scheduler, 'interval', seconds=900,
                  next_run_time=datetime.now())
scheduler.add_job(send_process, 'interval', seconds=30)
scheduler.start()
