#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import random

def get_kacho():
    list = [
        u"ちょっとまって",
        u"http://www.slideshare.net/bpstudy/bpstudy36-beproudbot-5319457",
    ]
    return list[random.randint(0, len(list) - 1)]

if __name__ == "__main__":
    main()

