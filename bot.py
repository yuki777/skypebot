#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import Skype4Py
import random
import time
import datetime
from datetime import date
from time import strptime
import urllib
import lxml.html
import md5
import os.path

def handler(msg, event):
    if event == u"RECEIVED":
        if msg.Body:
            reply_message = get_reply_message(msg)
            if not reply_message:
                return False

            return msg.Chat.SendMessage(reply_message)

def get_reply_message(msg):
    if not msg:
        return False

    type = get_type(msg)
    if not type:
        return False

    reply_message = get_message_by_type(msg, type)
    if not reply_message:
        return False

    return reply_message

def get_message_by_type(msg, type):
    if not type:
        return False

    if type == "normal":
        return False

    if type == "help":
        return get_help()

    if type == "uranai":
        return get_uranai(msg)

    if type == "snap":
        return get_snap(msg)

    if type == "tenki":
        return get_tenki(msg)

    if type == "unko":
        return get_unko(msg)

    if type == "jisin":
        return get_jisin(msg)

    if type == "kacho":
        return get_kacho()

    if type == "increment":
        return increment(msg)

    if type == "decrement":
        return decrement(msg)

    return False

def decrement(msg):
    cut = len(msg.Body) - 2
    maybe_user = msg.Body[0:cut]
    user = get_user_by_contacts(maybe_user)
    if not user:
        return False

    point_dir = '/tmp/skype_user_point/' 
    m = md5.new()
    m.update(user)
    user_file = point_dir + m.hexdigest()

    if not os.path.isfile(user_file):
        f = open(user_file, mode='w')
        f.write(u"-1")
        f.close
        return user + " : -1"

    f = open(user_file, mode='r')
    point = f.read() 
    point = int(point)
    point -= 1
    f.close()
    f = open(user_file, mode='w')
    f.write(str(point))
    f.close()

    return user + " : " + str(point)

def get_user_by_contacts(user):
    contacts = (
        "yuki.mazda",
        "bot.notify",
        "oyokawa.k",
    )
    if not user in contacts:
        return False

    return user

def increment(msg):
    cut = len(msg.Body) - 2
    maybe_user = msg.Body[0:cut]
    user = get_user_by_contacts(maybe_user)
    if not user:
        return False

    point_dir = '/tmp/skype_user_point/' 
    m = md5.new()
    m.update(user)
    user_file = point_dir + m.hexdigest()

    if not os.path.isfile(user_file):
        f = open(user_file, mode='w')
        f.write(u"1")
        f.close
        return user + " : 1"

    f = open(user_file, mode='r')
    point = f.read() 
    point = int(point)
    point += 1
    f.close()
    f = open(user_file, mode='w')
    f.write(str(point))
    f.close()

    return user + " : " + str(point)

def get_kacho():
    list = [
        u"ちょっとまって",
        u"http://www.slideshare.net/bpstudy/bpstudy36-beproudbot-5319457",
    ]
    return list[random.randint(0, len(list) - 1)]

def get_uranai(msg):
    seiza = {
        1  : {'id' : 'cp', 'name' : u'山羊座'},
        2  : {'id' : 'aq', 'name' : u'水瓶座'},
        3  : {'id' : 'pi', 'name' : u'魚座'},
        4  : {'id' : 'ar', 'name' : u'牡羊座'},
        5  : {'id' : 'ta', 'name' : u'牡牛座'},
        6  : {'id' : 'ge', 'name' : u'双子座'},
        7  : {'id' : 'ca', 'name' : u'蟹座'},
        8  : {'id' : 'le', 'name' : u'獅子座'},
        9  : {'id' : 'vi', 'name' : u'乙女座'},
        10 : {'id' : 'li', 'name' : u'天秤座'},
        11 : {'id' : 'sc', 'name' : u'蠍座'},
        12 : {'id' : 'sa', 'name' : u'射手座'}
    }

    if not msg.Sender.Birthday:
        return False

    s = str(msg.Sender.Birthday)
    dobj = date(*strptime(s, "%Y-%m-%d")[0:3])
    year, month, day = dobj.year, dobj.month, dobj.day

    if day > 22:
        if month == 12:
            my_seiza = seiza[1]
        else:
            my_seiza = seiza[month + 1]
    else :
        my_seiza = seiza[month]

    if not my_seiza:
        return False

    url = "http://woman.excite.co.jp/fortune/horoscopes/sign_" + my_seiza['id']
    fd = urllib.urlopen(url)
    s = fd.read().decode('utf-8')
    xRoot = lxml.html.fromstring(s)

    # 概要文言
    x = xRoot.xpath('//*[@id="horoscope"]/div/div[4]/div/p[1]/text()')
    uranai_desc = x[0]

    # 総合運ポイント
    #x = xRoot.get_element_by_id('horoscope_all')
    #uranai_point = x.text_content()
    x = xRoot.xpath('//*[@id="horoscope"]/div/div[2]/div/dl[1]/dd[1]/span')
    uranai_point = x[0].text

    ## ランキング
    #x = xRoot.get_element_by_id('horoscope_ranking')
    #uranai_ranking = x.text_content()
    x = xRoot.xpath('//*[@id="horoscope"]/div/div[2]/div/dl[1]/dd[2]/a/span')
    uranai_ranking = x[0].text

    # 今日
    today = datetime.datetime.now().strftime('%Y/%m/%d')

    return u"今日の占い " + today + "\n\n" + my_seiza['name'] + u" " + uranai_point + u"点, " + uranai_ranking + u"位\n\n" + uranai_desc + u"\n" + url + u"\n"

def get_snap(msg):
    url = "http://www.excite.co.jp"
    fd = urllib.urlopen(url)
    s = fd.read().decode('utf-8')
    xRoot = lxml.html.fromstring(s)

    # 今日のsnapのURLを取得
    x = xRoot.xpath('//*[@id="snap"]/div[2]/a/@href')
    todays_snap_url = x[0]

    # モデルの名前などを取得
    url = todays_snap_url
    fd = urllib.urlopen(url)
    s = fd.read().decode('utf-8')
    xRoot = lxml.html.fromstring(s)
    x = xRoot.xpath('//*[@id="l_wrapper"]/div[1]/div[3]/p/text()')
    name = x[1]

    # ファッションポイントを取得
    x = xRoot.xpath('//*[@id="l_wrapper"]/div[1]/div[2]/div[2]/dl/dt/text()')
    fashion_point = x[0]

    # ファッションポイント詳細を取得
    x = xRoot.xpath('//*[@id="l_wrapper"]/div[1]/div[2]/div[2]/dl/dd/text()')
    fashion_point_detail = x[0]

    # 今日
    today = datetime.datetime.now().strftime('%Y/%m/%d')

    return u" 今日のスナップ " + today + "\n\n" + name + u"\n" + fashion_point + u"\n\n" + fashion_point_detail + u"\n" + todays_snap_url + u"\n"

# 今日の天気
def get_tenki(msg):
    url = "http://weather.excite.co.jp/area/ar-4410/"
    fd = urllib.urlopen(url)
    s = fd.read().decode('utf-8')
    xRoot = lxml.html.fromstring(s)
    x = xRoot.xpath('//*[@id="todayWeather"]/p')
    todays_tenki = x[0].text
    x = xRoot.xpath('//*[@id="todayWeather"]/div[1]/p/text()[1]')
    todays_date = x[0]

    return todays_date + todays_tenki 

# 運行情報
def get_unko(msg):
    url = "http://www.tokyometro.jp/unkou/"
    fd = urllib.urlopen(url)
    s = fd.read().decode('utf-8')
    xRoot = lxml.html.fromstring(s)
    x = xRoot.xpath('//*[@id="mainArea"]/div[1]/div/div/div/div/div[2]/table/tbody/tr[4]/td[2]/p')
    return u" (開発中) "

# 地震
def get_jisin(msg):
    url = "http://www.jma.go.jp/jp/quake/quake_singen_index.html"
    fd = urllib.urlopen(url)
    s = fd.read().decode('utf-8')
    xRoot = lxml.html.fromstring(s)
    x = xRoot.xpath('//*[@id="info"]/table/tbody/tr[2]/td[4]')
    return u" (開発中) "

def get_help():
    return """
#help       使い方を返します。
#uranai     あなたの今日の占いを返します。
#snap       今日のsnapを返します。
#tenki      今日の天気を返します。
#unko       電車の運行情報を返します。
#jisin      地震情報を返します。
#kacho      課長
skype_id++  インクリメントします。
skype_id--  デクリメントします。
    """

def get_type(msg):
    if not msg.Body:
        return False

    if msg.Body[0:] == "#help":
        return "help"

    if msg.Body[0:] == "#uranai":
        return "uranai"

    if msg.Body[0:] == "#snap":
        return "snap"

    if msg.Body[0:] == "#tenki":
        return "tenki"

    if msg.Body[0:] == "#unko":
        return "unko"

    if msg.Body[0:] == "#jisin":
        return "jisin"

    if msg.Body[0:] == "#kacho":
        return "kacho"

    if msg.Body.endswith("++"):
        return "increment"

    if msg.Body.endswith("--"):
        return "decrement"

def main():
    skype = Skype4Py.Skype(Transport='x11')
    skype.OnMessageStatus = handler
    skype.Attach()
    while True:
        time.sleep(1) 

if __name__ == "__main__":
    main()

