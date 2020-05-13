
import requests
import datetime
# from collections import namedtuple
from app.bot_sender import TelegramSend
from app import db  # bot, app
from app.models import Post as PostModel, VkPublic, Task
import json


class Api:

    base = 'https://api.vk.com/method/'

    def __init__(self, access_token, v='5.103'):
        self.access_token = access_token
        self.v = v
        self.method = ''

    def __getattr__(self, attrname):
        self.method += attrname + '.'
        return self

    def __call__(self, *args, **kwargs):
        url = self.base + self.method[:-1]
        self.method = ''
        kwargs['access_token'] = self.access_token
        kwargs['v'] = self.v
        a = requests.post(url=url, data=kwargs)
        return a.json()


class Post:
    '''

    '''
    # text = ''
    # marked_as_ads = False
    # post_type = 'post'
    # date = None
    # photo = []
    # video = []  # TODO:
    # audio = []
    # doc = []  # TODO:
    # link = []  # TODO:
    # note = []  # TODO:
    # poll = []  # TODO:
    # page = []  # TODO:
    # album = []  # TODO:
    # _photos_list = []
    # _market = []
    # _market_album = []
    # _sticker = []
    # _pretty_cards = []

    def __init__(self, input_json: dict, from_db=False):
        self.photo = []
        self.text = ''
        self.audio = []
        self.id = input_json['id']
        try:
            self.date = str(datetime.datetime.utcfromtimestamp(
                int(input_json['date'])))
        except:
            self.date = input_json['date']

        if from_db:
            if input_json.get('id'):
                self.id = input_json['id']
            if input_json.get('text'):
                self.text = input_json['text']
            if input_json.get('photo'):
                self.photo = input_json['photo']
            if input_json.get('audio'):
                self.audio = input_json['audio']
        else:
            if input_json.get('text'):
                self.text = input_json['text']
            if input_json.get('marked_as_ads'):
                self.marked_as_ads = True
            if input_json.get('post_type'):
                self.post_type = input_json['post_type']
            if input_json.get('attachments'):
                for attach in input_json['attachments']:
                    if attach['type'] == 'photo':
                        biggest_size = 0
                        url = ''
                        for size in attach['photo']['sizes']:
                            if size['height'] >= biggest_size:
                                url = size['url']
                        self.photo.append(url)
                    if attach['type'] == 'video':
                        # cложная тема с аксес токенами
                        pass
                    if attach['type'] == 'audio':
                        a = {'artist': attach['audio']['artist'],
                             'title': attach['audio']['title'],
                             'url': attach['audio']['url']}
                        self.audio.append(a)

            # if not hasattr(self, 'text'):
            #     self.text = None
            # if not hasattr(self, 'photo'):
            #     self.photo = None
            # if not hasattr(self, 'audio'):
            #     self.audio = None
    def save(self):
        try:
            data_json = {'id': self.id, 'photo': self.photo, 'audio': self.audio,
                         'text': self.text, 'date': self.date}
            a = PostModel(internal_id=self.id, data_json=json.dumps(data_json))
            db.session.add(a)
            db.session.commit()
        except Exception as e:
            print(e)
            data_json = {'id': self.id, 'photo': self.photo[0], 'audio': self.audio,
                         'text': self.text[:500], 'date': self.date}
            print(data_json)
            a = PostModel(internal_id=self.id, data_json=json.dumps(data_json))
            db.session.add(a)
            db.session.commit()


    # def send(self, tg_api, tg_channel, bot_token):
    #     tg_api.send([self])


class VK_public:
    '''
    address - короткое название паблика, н-р super_ussr
    bot_token - токен бота для постинга, н-р оjdjhG767GHkjj&799KHGVKJ
    last_posts - последние 20 постов паблика, в формате json, \
    н-р [{пост_в_формате_апи_вк}, {...}, ...]
    tg_channel - название канала телеги куда постить, н-р @svalko (без @)
    '''

    def __init__(self, vk_pub):
        self.address = vk_pub.address
        self.bot_token = vk_pub.bot_token
        # self.last_posts = vk_pub.last_posts
        self.tg_channel = vk_pub.tg_channel

    def download_last_posts(self, api, n=20):
        res = api.wall.get(domain=self.address, count=n)
        res = res['response']['items']
        extracted_posts = [Post(x) for x in res]
        # print(extracted_posts)
        return extracted_posts

    def get_last_posts(self, n=20):
        posts = PostModel.query.all()
        parced_posts = []
        for post in posts:
            parced_json = json.loads(post.data_json)
            parced_posts.append(Post(parced_json))
        # posts = []
        return parced_posts

    def save_unsaved_post(self, posts: list):
        '''
        return not tg-posted posts
        '''
        saved_posts = self.get_last_posts()
        saved_ids = [x.id for x in saved_posts]
        new_ids = [x.id for x in posts]
        unsaved_ids = [x for x in new_ids if x not in saved_ids]
        new_posts = []
        if unsaved_ids:
            for post in posts:
                if post.id in unsaved_ids:
                    post.save()
                    new_posts.append(post)
        return new_posts

    def send_new_posts(self, posts: list):
        if posts:
            for post in posts:
                new_task = Task(post_id=post.id, bot_token=self.bot_token,
                                tg_channel=self.tg_channel)
                db.session.add(new_task)
            db.session.commit()

            # success = False
            # while not success:
            #     try:
            #         print('start sending')
            #         tg_api = TelegramSend(self.bot_token, self.tg_channel)
            #         tg_api.send([post])
            #         success = True
            #     except Exception as e:
            #         print(e)
        return len(posts)


# Pub = namedtuple('Pub', ['address', 'bot_token', 'tg_channel'])
# vk_pub = Pub(address='onlyorly',
#              bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
#              tg_channel='@novostibyte')

# arr_of_publics = []
# arr_of_publics.append(VK_public(vk_pub))

# api = Api('85b94daf85b94daf85b94daf2e85c8262e885b985b94dafdb1c75e53197a87568527221')

# for pub in arr_of_publics:
#     extracted_posts = pub.download_last_posts(api)
#     new_posts = pub.save_unsaved_post(extracted_posts)
#     tg_api = 0
#     pub.send_new_posts(tg_api, new_posts)
