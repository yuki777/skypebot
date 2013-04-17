#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import time
import datetime
import urllib
import lxml.html

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

if __name__ == "__main__":
    main()

