from app import app, db  # bot,
from app.models import Post, VkPublic
from apscheduler.schedulers.background import BackgroundScheduler
# import requests
# import re
# from bs4 import BeautifulSoup
# import json
# import telegram
from datetime import datetime
from app.parcer import VK_public, Api


def make_things_with_public(vk_pub):
    # Pub = namedtuple('Pub', ['address', 'bot_token', 'tg_channel'])
    # vk_pub = Pub(address='onlyorly',
    #              bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
    #              tg_channel='@novostibyte')

    # arr_of_publics = []
    # arr_of_publics.append(VK_public(vk_pub))

    api = Api('85b94daf85b94daf85b94daf2e85c8262e885b985b94dafdb1c75e53197a87568527221')

    # for pub in arr_of_publics:

    pub = VK_public(vk_pub)

    extracted_posts = pub.download_last_posts(api)
    new_posts = pub.save_unsaved_post(extracted_posts)
    tg_api = 0
    pub.send_new_posts(tg_api, new_posts)


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
        # a = VkPublic(address='overhear',
        #              bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
        #              tg_channel='@vk_podslushano')
        b = VkPublic(address='mayland',
                     bot_token='873231530:AAEHeyyyNICXFBpbc8FpHleGJjQgP-OC81c',
                     tg_channel='@vk_podslushano')
        db.session.add(b)
        # db.session.add(a)
        db.session.commit()
        # make_things_with_public(a)
        make_things_with_public(b)

    # im, an = parcer()
    # try:
    #     data_from_db = SaveData.query.all()
    #     if len(data_from_db) > 1:
    #         print('More than one record in db.')
    #         saved_data = SaveData.query.first().data
    #         SaveData.query.delete()
    #         new_data = SaveData(data=saved_data)
    #         db.session.add(new_data)
    #         db.session.commit()
    #     data = SaveData.query.first()
    #     print(f'Data in try: {data}')
    # except Exception as e:
    #     print(str(e))
    #     a = SaveData(
    #         data='[{"URL": "https://svalko.org/data/2020_04_02_15_26pixmafia_com_post_2020_03_005751_daily_picdump_005751_030.jpg", "Send": true, "Post_url": "https://svalko.org/775571.html"}, {"URL": "https://svalko.org/data/2020_04_02_15_23cdn_remotvet_ru_files_users_images_61_d6_61d60f305e52b0cd1f6886117ca06715.jpg", "Send": true, "Post_url": "https://svalko.org/775570.html"}, {"URL": "https://svalko.org/data/2020_04_02_15_15sun1_99_userapi_com_LJd8ZpzuEICXeC5b7XunPfwwX_y_YbPRBeGkNw_cnEI1gOWacM.jpg", "Send": true, "Post_url": "https://svalko.org/775568.html"}, {"URL": "/data/gif-previews/2020_04_02_15_06cs13_pikabu_ru_post_img_2020_03_31_11_1585682191125198367.gif", "Send": true, "Post_url": "https://svalko.org/775564.html"}, {"URL": "https://svalko.org/data/2020_04_02_11_36cs10_pikabu_ru_post_img_big_2020_04_02_0_1585776360147935950.jpg", "Send": true, "Post_url": "https://svalko.org/775547.html"}, {"URL": "https://svalko.org/data/2020_03_31_14_0866_media_tumblr_com_cf894ad5f901d613545a410b10f97fbb_7483ad30d2899d48_cd_s1280x1920_b0292f1c6f7f821349386ad62fe646116becbfcc.jpg", "Send": true, "Post_url": "https://svalko.org/775347.html"}, {"URL": "https://svalko.org/data/2020_03_31_14_0366_media_tumblr_com_9c24d7c7f289e0d28769a8e2f310810b_169f0f8144d1a03b_f2_s540x810_468b2061bc58cba26796453c5ce41d7e1d4c2e54.jpg", "Send": true, "Post_url": "https://svalko.org/775346.html"}, {"URL": "https://svalko.org/data/2020_03_31_14_01images_vfl_ru_ii_1584081495_747945a0_29857758.jpg", "Send": false, "Post_url": "https://svalko.org/775345.html"}, {"URL": "https://svalko.org/data/2020_03_31_14_00pixmafia_com_post_2020_03_005773_daily_picdump_005773_042.jpg", "Send": true, "Post_url": "https://svalko.org/775344.html"}, {"URL": "https://svalko.org/data/2020_03_31_13_59neteye_ru_uploads_images_00_00_01_2016_01_18_7994a76b48.jpg", "Send": true, "Post_url": "https://svalko.org/775343.html"}, {"URL": "https://svalko.org/data/2020_03_31_13_58sun1_95_userapi_com_PYbIUphe3Erh1JnuCGo_vVWk_SeNssiPhh8ttA_qTxduxn5LD0.jpg", "Send": true, "Post_url": "https://svalko.org/775342.html"}, {"URL": "https://svalko.org/data/2020_03_31_13_57sun1_99_userapi_com_vXKOM1nUdfRGVcv6BcpetDNV2CRUUaSOt4UHCg_AzBI6XFOq5I.jpg", "Send": true, "Post_url": "https://svalko.org/775341.html"}, {"URL": "https://svalko.org/data/2020_03_31_13_56_970331_1.png", "Send": true, "Post_url": "https://svalko.org/775340.html"}, {"URL": "https://svalko.org/data/2020_03_31_01_17s_zefirka_net_images_2020_03_30_podborka_prikolnyx_kartinok_podborka_prikolnyx_kartinok_76.jpg", "Send": true, "Post_url": "https://svalko.org/775307.html"}, {"URL": "https://svalko.org/data/2020_03_29_02_47cdn_jpg_wtf_futurico_e6_3f_1585377439_e63f9e47ef82593991284c5ff0fcce16.jpeg", "Send": true, "Post_url": "https://svalko.org/775167.html"}, {"URL": "https://svalko.org/data/2020_03_28_13_59sun9_59_userapi_com_c858236_v858236970_170fda_AK8SkpYv3Z4.jpg", "Send": true, "Post_url": "https://svalko.org/775103.html"}, {"URL": "https://svalko.org/data/2020_03_28_13_54i_imgur_com_UxXC2Lp.jpg", "Send": true, "Post_url": "https://svalko.org/775101.html"}, {"URL": "/data/gif-previews/2020_03_28_13_48cdn_ebaumsworld_com_mediaFiles_picture_604025_86190751.gif", "Send": true, "Post_url": "https://svalko.org/775096.html"}, {"URL": "https://svalko.org/data/2020_03_26_15_29sun9_3_userapi_com_c621515_v621515671_1889e_iipN3aNnkHo.jpg", "Send": true, "Post_url": "https://svalko.org/774906.html"}, {"URL": "https://svalko.org/data/2020_03_26_15_27s_zefirka_net_images_2020_03_24_podborka_prikolnyx_kartinok_podborka_prikolnyx_kartinok_101.jpg", "Send": true, "Post_url": "https://svalko.org/774904.html"}, {"URL": "https://svalko.org/data/2020_03_25_18_03sun9_69_userapi_com_c543100_v543100097_36123_cTq_xj7Ua3k.jpg", "Send": true, "Post_url": "https://svalko.org/774801.html"}, {"URL": "https://svalko.org/data/2020_03_24_16_2866_media_tumblr_com_e42e7d4ab819fa94ac89e534cbd605fd_4a23649b84112b0f_59_s1280x1920_61cba0d1c0ad6fa6a986fbe7ed482b99214af318.jpg", "Send": true, "Post_url": "https://svalko.org/774636.html"}, {"URL": "https://svalko.org/data/2020_03_24_16_2666_media_tumblr_com_7c3f06d183f6d4299b77c55eb8a5a797_7a16cd2282eea507_87_s640x960_4fe67a20cb80ff5cd4307a00a777653a8ca7aa0c.jpg", "Send": true, "Post_url": "https://svalko.org/774634.html"}, {"URL": "https://svalko.org/data/2020_03_23_13_53pbs_twimg_com_media_ETvVix_X0AAf0Q8.jpg", "Send": true, "Post_url": "https://svalko.org/774454.html"}, {"URL": "https://svalko.org/data/2020_03_23_10_55sun1_47_userapi_com_dpZ4IJJVggNKxBsAKpzIhb3bOs8R4x1R7_gjkA_tYxxilUKPVU.jpg", "Send": true, "Post_url": "https://svalko.org/774426.html"}, {"URL": "https://svalko.org/data/2020_03_23_10_54sun1_98_userapi_com_GsNqGKZPmebAfS0KsYxgmTGH4L0e0PT3pzATdA_gekeaVL_XGA.jpg", "Send": true, "Post_url": "https://svalko.org/774425.html"}, {"URL": "https://svalko.org/data/2020_03_23_11_1566_media_tumblr_com_643ccccc2cf742ef6c0f1761cbacb6c6_00f9df3de98be93c_0f_s1280x1920_01b79608ea3e432898ea1a8cb3093985edcb1895.jpg", "Send": true, "Post_url": "https://svalko.org/774424.html"}, {"URL": "https://svalko.org/data/2020_03_23_10_48_111570_1.jpeg", "Send": true, "Post_url": "https://svalko.org/774422.html"}]')
    #     db.session.add(a)
    #     db.session.commit()
    #     data = SaveData.query.first()
    #     print(f'Data in except main_func: {data}')


    # if not data:
    #     print('Data is empty, create new data in db...')
    #     a = SaveData(data='[{"URL": "https://svalko.org/data/2020_04_02_15_26pixmafia_com_post_2020_03_005751_daily_picdump_005751_030.jpg", "Send": true, "Post_url": "https://svalko.org/775571.html"}, {"URL": "https://svalko.org/data/2020_04_02_15_23cdn_remotvet_ru_files_users_images_61_d6_61d60f305e52b0cd1f6886117ca06715.jpg", "Send": true, "Post_url": "https://svalko.org/775570.html"}, {"URL": "https://svalko.org/data/2020_04_02_15_15sun1_99_userapi_com_LJd8ZpzuEICXeC5b7XunPfwwX_y_YbPRBeGkNw_cnEI1gOWacM.jpg", "Send": true, "Post_url": "https://svalko.org/775568.html"}, {"URL": "/data/gif-previews/2020_04_02_15_06cs13_pikabu_ru_post_img_2020_03_31_11_1585682191125198367.gif", "Send": true, "Post_url": "https://svalko.org/775564.html"}, {"URL": "https://svalko.org/data/2020_04_02_11_36cs10_pikabu_ru_post_img_big_2020_04_02_0_1585776360147935950.jpg", "Send": true, "Post_url": "https://svalko.org/775547.html"}, {"URL": "https://svalko.org/data/2020_03_31_14_0866_media_tumblr_com_cf894ad5f901d613545a410b10f97fbb_7483ad30d2899d48_cd_s1280x1920_b0292f1c6f7f821349386ad62fe646116becbfcc.jpg", "Send": true, "Post_url": "https://svalko.org/775347.html"}, {"URL": "https://svalko.org/data/2020_03_31_14_0366_media_tumblr_com_9c24d7c7f289e0d28769a8e2f310810b_169f0f8144d1a03b_f2_s540x810_468b2061bc58cba26796453c5ce41d7e1d4c2e54.jpg", "Send": true, "Post_url": "https://svalko.org/775346.html"}, {"URL": "https://svalko.org/data/2020_03_31_14_01images_vfl_ru_ii_1584081495_747945a0_29857758.jpg", "Send": false, "Post_url": "https://svalko.org/775345.html"}, {"URL": "https://svalko.org/data/2020_03_31_14_00pixmafia_com_post_2020_03_005773_daily_picdump_005773_042.jpg", "Send": true, "Post_url": "https://svalko.org/775344.html"}, {"URL": "https://svalko.org/data/2020_03_31_13_59neteye_ru_uploads_images_00_00_01_2016_01_18_7994a76b48.jpg", "Send": true, "Post_url": "https://svalko.org/775343.html"}, {"URL": "https://svalko.org/data/2020_03_31_13_58sun1_95_userapi_com_PYbIUphe3Erh1JnuCGo_vVWk_SeNssiPhh8ttA_qTxduxn5LD0.jpg", "Send": true, "Post_url": "https://svalko.org/775342.html"}, {"URL": "https://svalko.org/data/2020_03_31_13_57sun1_99_userapi_com_vXKOM1nUdfRGVcv6BcpetDNV2CRUUaSOt4UHCg_AzBI6XFOq5I.jpg", "Send": true, "Post_url": "https://svalko.org/775341.html"}, {"URL": "https://svalko.org/data/2020_03_31_13_56_970331_1.png", "Send": true, "Post_url": "https://svalko.org/775340.html"}, {"URL": "https://svalko.org/data/2020_03_31_01_17s_zefirka_net_images_2020_03_30_podborka_prikolnyx_kartinok_podborka_prikolnyx_kartinok_76.jpg", "Send": true, "Post_url": "https://svalko.org/775307.html"}, {"URL": "https://svalko.org/data/2020_03_29_02_47cdn_jpg_wtf_futurico_e6_3f_1585377439_e63f9e47ef82593991284c5ff0fcce16.jpeg", "Send": true, "Post_url": "https://svalko.org/775167.html"}, {"URL": "https://svalko.org/data/2020_03_28_13_59sun9_59_userapi_com_c858236_v858236970_170fda_AK8SkpYv3Z4.jpg", "Send": true, "Post_url": "https://svalko.org/775103.html"}, {"URL": "https://svalko.org/data/2020_03_28_13_54i_imgur_com_UxXC2Lp.jpg", "Send": true, "Post_url": "https://svalko.org/775101.html"}, {"URL": "/data/gif-previews/2020_03_28_13_48cdn_ebaumsworld_com_mediaFiles_picture_604025_86190751.gif", "Send": true, "Post_url": "https://svalko.org/775096.html"}, {"URL": "https://svalko.org/data/2020_03_26_15_29sun9_3_userapi_com_c621515_v621515671_1889e_iipN3aNnkHo.jpg", "Send": true, "Post_url": "https://svalko.org/774906.html"}, {"URL": "https://svalko.org/data/2020_03_26_15_27s_zefirka_net_images_2020_03_24_podborka_prikolnyx_kartinok_podborka_prikolnyx_kartinok_101.jpg", "Send": true, "Post_url": "https://svalko.org/774904.html"}, {"URL": "https://svalko.org/data/2020_03_25_18_03sun9_69_userapi_com_c543100_v543100097_36123_cTq_xj7Ua3k.jpg", "Send": true, "Post_url": "https://svalko.org/774801.html"}, {"URL": "https://svalko.org/data/2020_03_24_16_2866_media_tumblr_com_e42e7d4ab819fa94ac89e534cbd605fd_4a23649b84112b0f_59_s1280x1920_61cba0d1c0ad6fa6a986fbe7ed482b99214af318.jpg", "Send": true, "Post_url": "https://svalko.org/774636.html"}, {"URL": "https://svalko.org/data/2020_03_24_16_2666_media_tumblr_com_7c3f06d183f6d4299b77c55eb8a5a797_7a16cd2282eea507_87_s640x960_4fe67a20cb80ff5cd4307a00a777653a8ca7aa0c.jpg", "Send": true, "Post_url": "https://svalko.org/774634.html"}, {"URL": "https://svalko.org/data/2020_03_23_13_53pbs_twimg_com_media_ETvVix_X0AAf0Q8.jpg", "Send": true, "Post_url": "https://svalko.org/774454.html"}, {"URL": "https://svalko.org/data/2020_03_23_10_55sun1_47_userapi_com_dpZ4IJJVggNKxBsAKpzIhb3bOs8R4x1R7_gjkA_tYxxilUKPVU.jpg", "Send": true, "Post_url": "https://svalko.org/774426.html"}, {"URL": "https://svalko.org/data/2020_03_23_10_54sun1_98_userapi_com_GsNqGKZPmebAfS0KsYxgmTGH4L0e0PT3pzATdA_gekeaVL_XGA.jpg", "Send": true, "Post_url": "https://svalko.org/774425.html"}, {"URL": "https://svalko.org/data/2020_03_23_11_1566_media_tumblr_com_643ccccc2cf742ef6c0f1761cbacb6c6_00f9df3de98be93c_0f_s1280x1920_01b79608ea3e432898ea1a8cb3093985edcb1895.jpg", "Send": true, "Post_url": "https://svalko.org/774424.html"}, {"URL": "https://svalko.org/data/2020_03_23_10_48_111570_1.jpeg", "Send": true, "Post_url": "https://svalko.org/774422.html"}]')
    #     db.session.add(a)
    #     db.session.commit()
    # data = SaveData.query.first()
    # data = json.loads(data.data)
    # print(f'Data is {data}')

    # rec_image = im
    # rec_caption = an

    # print('Cycle start...')
    # for item_rec, item_cap in zip(rec_image, rec_caption):
    #     for item_json in data:
    #         if item_json['URL'] == item_rec:
    #             print('Image parameters already in the data.')
    #             break
    #     else:
    #         print('Add new images in data.')
    #         data.append({'URL': item_rec, 'Send': False, 'Post_url': item_cap})
    # # print('')
    # for item in data:
    #     if not item['Send']:
    #         print('Some item is not send, try sending...')
    #         # try:
    #         if item['URL'].split('.')[-1] == 'gif':
    #             print('Oh, im find a gif!')
    #             t = item['URL'].partition('/gif-previews')
    #             full_gif = str('https://svalko.org/' + t[0] + t[2])
    #             if item.get('Post_url'):
    #                 print('Send animation')
    #                 try:
    #                     bot.sendAnimation('@svalko_org', full_gif, caption=item.get('Post_url'))
    #                 except Exception as e:
    #                     print(f'Halp! I find some error. Reason: {e}')

    #             else:
    #                 print('Uff, cant find url for gif post, sending without url...')
    #                 try:
    #                     bot.sendAnimation('@svalko_org', full_gif)
    #                 except Exception as e:
    #                     print(f'Halp! I find some error. Reason: {e}')
    #             item['Send'] = True
    #             print(f'Update status successful for gif {item["URL"]}')
    #         else:
    #             if item.get('Post_url'):
    #                 print(f'Sending photo {item["URL"]}')
    #                 try:
    #                     bot.sendPhoto('@svalko_org', item['URL'], caption=item.get('Post_url'))
    #                 except Exception as e:
    #                     print(f'Halp! I find some error. Reason: {e}')
    #             else:
    #                 print('Uff, cant find url for img post, sending without url...')
    #                 try:
    #                     bot.sendPhoto('@svalko_org', item['URL'])
    #                 except Exception as e:
    #                     print(f'Halp! I find some error. Reason: {e}')
    #         item['Send'] = True
    #         print(f'Update status successful for img {item["URL"]}')

    # data_db = SaveData.query.first()
    # data_db.data = json.dumps(data)
    # db.session.commit()
    # print(f'Save update version of json like: {data_db.data}')



    pass

    
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
scheduler.start()
