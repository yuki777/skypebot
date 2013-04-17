#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import urllib
import lxml.html

# 運行情報
def get_unko(msg):
    url = "http://www.tokyometro.jp/unkou/"
    fd = urllib.urlopen(url)
    s = fd.read().decode('utf-8')
    xRoot = lxml.html.fromstring(s)
    x = xRoot.xpath('//*[@id="mainArea"]/div[1]/div/div/div/div/div[2]/table/tbody/tr[4]/td[2]/p')
    return u" (開発中) "

if __name__ == "__main__":
    main()

