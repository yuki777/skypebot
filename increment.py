#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import md5
import os.path

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

if __name__ == "__main__":
    main()

