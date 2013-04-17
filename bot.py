#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# libs
import Skype4Py
import time

# my libs
import help
import uranai
import kacho
import snap
import tenki
import unko
import jisin
import increment
import decrement

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
    if not type: return False

    if type == "normal":    return False
    if type == "help":      return help.get_help()
    if type == "uranai":    return uranai.get_uranai(msg)
    if type == "snap":      return snap.get_snap(msg)
    if type == "tenki":     return tenki.get_tenki(msg)
    if type == "unko":      return unko.get_unko(msg)
    if type == "jisin":     return jisin.get_jisin(msg)
    if type == "kacho":     return kacho.get_kacho()
    if type == "increment": return increment.increment(msg)
    if type == "decrement": return decrement.decrement(msg)

    return False

def get_type(msg):
    if not msg.Body: return False

    if msg.Body[0:] == "#help":   return "help"
    if msg.Body[0:] == "#uranai": return "uranai"
    if msg.Body[0:] == "#snap":   return "snap"
    if msg.Body[0:] == "#tenki":  return "tenki"
    if msg.Body[0:] == "#unko":   return "unko"
    if msg.Body[0:] == "#jisin":  return "jisin"
    if msg.Body[0:] == "#kacho":  return "kacho"
    if msg.Body.endswith("++"): return "increment"
    if msg.Body.endswith("--"): return "decrement"

def main():
    skype = Skype4Py.Skype(Transport='x11')
    skype.OnMessageStatus = handler
    skype.Attach()
    while True:
        time.sleep(1) 

if __name__ == "__main__":
    main()

