# -*- coding: utf-8 -*-
import requests
import json

requests.adapters.DEFAULT_RETRIES = 5

NEWS_API_ENDPOINT = 'https://newsapi.org/v1/'
NEWS_API_KEY = '2027a8a068ed45b8811d6e2e3f7a32e9'
ARTICLES_API = 'articles'

CNN = 'cnn'
DEFAULT_SOURCES = [CNN]
SORT_BY_TOP = 'top'

def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=ARTICLES_API):
    return end_point + api_name

# {
# "status": "ok",
# "source": "the-verge",
# "sortBy": "top",
# -"articles": [
# -{
# "author": "Vlad Savov",
# "title": "LG’s V30S ThinQ is a V30 with more RAM and AI",
# "description": "Smartphones don’t get much more repetitive than this",
# "url": "https://www.theverge.com/2018/2/24/17048574/lg-v30s-price-release-date-mwc-2018",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/wfC111h77ywiZGQVFm4guyZIGQE=/0x231:2040x1299/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/10292177/lg_v30s_vladsavovmwc18.jpg",
# "publishedAt": "2018-02-24T23:49:10Z"
# },
# -{
# "author": "Vlad Savov",
# "title": "Samsung’s Galaxy S9 launch video leaks out",
# "description": "Samsung’s Galaxy S9 launch video for MWC 2018 has been posted early, revealing the device’s specs and features",
# "url": "https://www.theverge.com/2018/2/24/17048814/samsung-galaxy-s9-mwc-2018-launch-video-leak",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/QcPprQnXS_H800uecLNizE5guks=/0x130:1800x1072/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/10291863/sgs9leak.jpg",
# "publishedAt": "2018-02-24T21:43:03Z"
# },
# -{
# "author": "Vlad Savov",
# "title": "MWC 2018: what to expect from Samsung, Nokia, and Sony in Barcelona",
# "description": "Hosted in Barcelona every year, Mobile World Congress plays host to some of the biggest Android flagship launches, and this year’s no different with Samsung preparing to unveil its new Galaxy S9. Over the years, Nokia, HTC, Sony, and LG have all competed with Samsung for the spotlight, but this year all the leaks, hype, and interest have been soaked up by the next pair of Galaxy devices.",
# "url": "https://www.theverge.com/2018/2/23/17043736/mwc-2018-preview-dates-schedule-barcelona-samsung-lg-sony",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/8si7Xv-EvtPehVevEophhnvOpHo=/0x73:1020x607/fit-in/1200x630/cdn.vox-cdn.com/assets/4044747/theverge1_1020.jpg",
# "publishedAt": "2018-02-23T12:30:08Z"
# },
# -{
# "author": "Tasha Robinson",
# "title": "Annihilation review: the most thoughtful science fiction movie since Arrival",
# "description": "The latest film from Ex Machina writer-director Alex Garland again digs deep into heady philosophical questions. The film follows characters played by Natalie Portman, Jennifer Jason Leigh, and Tessa Thompson into the heart of an eerie alien anomaly, in a plot that echoes the Russian movie Stalker.",
# "url": "https://www.theverge.com/2018/2/23/17042290/annihilation-review-natalie-portman-oscar-isaac-alex-garland-jeff-vandermeer",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/u9Wgpk8Yp6qRIG3CEX3JlNSYfHw=/0x0:7952x4163/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/10280433/anh_09225r.jpg",
# "publishedAt": "2018-02-23T15:37:31Z"
# },
# -{
# "author": "Paul Miller",
# "title": "The simple joy of projecting a horse on your friend",
# "description": "Anker’s Nebula Capsule portable projector has a terrible remote, but I learned a valuable lesson about how much fun it is to project video game speedruns onto people.",
# "url": "https://www.theverge.com/circuitbreaker/2018/2/24/17038214/anker-nebula-capsule-portable-projector-review",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/PSJj1umRBFUSRW9_SEOVGmcIUJ0=/0x146:2040x1214/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/10288123/akrales_180223_2330_0004.jpg",
# "publishedAt": "2018-02-24T20:00:02Z"
# },
# -{
# "author": "Angela Chen",
# "title": "The rapper Dessa scanned her brain to fall out of love",
# "description": "Rapper Dessa is a member of the indie hip-hop collective Doomtree, and she now has four solo albums and a Hamilton mixtape song under her belt. Haunted by a breakup, she turned to neuroscience to fall out of love and found answers that inform her new album, Chime.",
# "url": "https://www.theverge.com/2018/2/23/17021626/dessa-chime-music-neuroscience-psychology-love-philosophy",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/1enbQtIsIYMcGmOfQ2BMGf0eLgs=/0x292:2040x1360/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/10284235/jbareham_180215_2306_0044_02.jpg",
# "publishedAt": "2018-02-23T17:37:46Z"
# },
# -{
# "author": "Jacob Kastrenakes",
# "title": "New trailers: Lost in Space reboot, Silicon Valley, Krypton, and more",
# "description": "Watch this week’s new trailers from Netflix, HBO, Syfy, and more",
# "url": "https://www.theverge.com/2018/2/24/17045208/new-trailers-lost-in-space-silicon-valley-krypton-and-more",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/W6F9rc3wiHNUaVpLRmXYggI-12c=/0x0:3891x2037/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/10286399/LIS_SG_102_00247R.jpg",
# "publishedAt": "2018-02-24T17:00:02Z"
# },
# -{
# "author": "Andrew J. Hawkins",
# "title": "Black Panther’s Wakanda is a transportation utopia with a dash of reality",
# "description": "Black Panther is a transit buff’s dream come true, with an array of cool planes, trains, and cars — and just a dash of reality to ensure these Afrofuturist dreams maintain some believability.",
# "url": "https://www.theverge.com/2018/2/23/17044448/black-panther-wakanda-maglev-train-hyperloop-transportation",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/OzaG1MufOuzIMkLN96lNuw7ltHs=/0x3:1132x596/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/10285139/0218_WI_APAFRO_02_sq.jpg",
# "publishedAt": "2018-02-23T19:05:20Z"
# },
# -{
# "author": "Micah Singleton",
# "title": "JLab’s Epic Sport earbuds are excellent workout headphones",
# "description": "The Epic Sport headphones are available to purchase for $99.",
# "url": "https://www.theverge.com/circuitbreaker/2018/2/25/17046000/jlab-epic-sport-earbuds-workout-headphones-review",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/GDhAWNGMGHEBniFkFtSUWH9MIwc=/0x146:2040x1214/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/10045711/akrales_180116_2215_0041.jpg",
# "publishedAt": "2018-02-25T14:00:01Z"
# },
# -{
# "author": "Sam Byford",
# "title": "Huawei’s new MateBook X Pro laptop has incredibly tiny bezels",
# "description": "The webcam is built into the keyboard",
# "url": "https://www.theverge.com/2018/2/25/17049094/huawei-matebook-x-pro-mediapad-m5-pro-release-date-mwc-2018",
# "urlToImage": "https://cdn.vox-cdn.com/thumbor/D2QCczVHfT7wXYz0EsGcL1t_2iQ=/0x41:2040x1109/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/10280501/tong_180223_2326_0018.jpg",
# "publishedAt": "2018-02-25T13:30:02Z"
# }
# ]
# }
def get_news_from_source(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []
    # 对每一个source发起http request请求
    for source in sources:
        payload = {'apiKey' : NEWS_API_KEY,
                   'source' : source,
                   'sortBy' : sortBy}
        # response = requests.get(buildUrl(), params=payload)
        try:
            response = requests.get(buildUrl(), params=payload)
        except Exception as e:
            print('An error occurred:{}'.format(e))
            continue

        res_json = json.loads(response.content)

        # 对response中的每一条news添加新闻源
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):

            for news in res_json['articles']:
                news['source'] = res_json['source']

            # 合并列表
            articles.extend(res_json['articles'])

    return articles
