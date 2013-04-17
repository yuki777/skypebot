#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import urllib
import lxml.html

# 地震
def get_jisin(msg):
    url = "http://www.jma.go.jp/jp/quake/quake_singen_index.html"
    fd = urllib.urlopen(url)
    s = fd.read().decode('utf-8')
    xRoot = lxml.html.fromstring(s)
    x = xRoot.xpath('//*[@id="info"]/table/tbody/tr[2]/td[4]')
    return u" (開発中) "

if __name__ == "__main__":
    main()

