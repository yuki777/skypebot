#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from datetime import date
from time import strptime
import urllib
import lxml.html
import datetime

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

if __name__ == "__main__":
    main()
