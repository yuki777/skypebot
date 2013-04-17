#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import urllib
import lxml.html

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

if __name__ == "__main__":
    main()

