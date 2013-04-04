#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

# http://flask.pocoo.org/
# http://a2c.bitbucket.org/flask/
# http://www.ninxit.com/blog/2011/03/04/flask-kiso/
# http://d.hatena.ne.jp/Johan511/20110326/1301099330
import Skype4Py
import time
import commands
import urllib
from flask import Flask, request, redirect, url_for

app = Flask(__name__)
app.skype = Skype4Py.Skype(Transport='x11')
app.skype.Attach()

@app.route("/")
def index():
    html  = ''
    html += '<!DOCTYPE html>'
    html += '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:og="http://ogp.me/ns#" xmlns:fb="http://ogp.me/ns/fb#">'
    html += '<head>'
    html += '<meta name="author" content="@yuki777">'
    html += '<meta charset="utf-8">'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    html += '<meta property="og:title" content="Skype bot.notify DEMO"/>'
    html += '<meta property="og:description" content="Skype bot.notify DEMO is a web service that enables to instantly send and receive skype notifications from the internet."/>'
    html += '<meta name="description" content="Skype bot.notify DEMO is a web service that enables to instantly send and receive skype notifications from the internet.">'
    html += '<meta property="og:type"        content="website"/>'
    html += '<meta property="og:url"         content="http://ec2-46-51-234-206.ap-northeast-1.compute.amazonaws.com/"/>'
    html += '<meta property="og:image"       content="http://ec2-46-51-234-206.ap-northeast-1.compute.amazonaws.com/img/icon_256.png"/>'
    html += '<meta property="og:site_name"   content="Skype bot.notify DEMO"/>'
    html += '<meta property="fb:admins"      content="727539870"/>'
    html += '<meta property="fb:app_id"      content="164754137015321"/>'
    html += '<title>Skype bot.notify DEMO</title>'
    html += '</head>'
    html += '<body>'

    # facebook jssdk
    #html += '<div id="fb-root"></div> <script>(function(d, s, id) { var js, fjs = d.getElementsByTagName(s)[0]; if (d.getElementById(id)) return; js = d.createElement(s); js.id = id; js.src = "//connect.facebook.net/ja_JP/all.js#xfbml=1&appId=164754137015321"; fjs.parentNode.insertBefore(js, fjs); }(document, \'script\', \'facebook-jssdk\'));</script>'

    html += '<h1>Skype bot.notify DEMO</h1>'
    html += '<p><a href="http://bit.ly/skype-bot">http://bit.ly/skype-bot</a></p>'
    html += 'Skype bot.notify DEMO is a web service that enables to instantly send and receive skype notifications from the internet.</p>'
    html += '<hr>'
    html += '<h2>setup your skype</h2>'
    html += '<ul>'
    html += '<li>Add "bot.notify" to your Skype Contact list.</li>'
    html += 'or'
    html += '<li>Allow messages from "Anyone".</li>'
    html += '</ul>'
    html += '<hr>'
    html += '<h2>POST</h2>'
    html += '<form action="/post/" method="post">'
    html += '<p>From : bot.notify</p>'
    html += '<p>To : <input type="text" name="name" placeholder="SKYPE ID" autofocus value=""></p>'
    html += '<p>Message : <textarea name="message" rows="10" cols="50" placeholder="MESSAGE"></textarea>'
    html += '<input type="submit">'
    html += '</form>'
    html += '<hr>'
    html += '<h2>GET</h2>'
    html += 'http://ec2-46-51-234-206.ap-northeast-1.compute.amazonaws.com/(SKYPE ID)/(MESSAGE)'
    html += '<hr>'
    html += '<h2>curl</h2>'
    html += '<p>MESSAGE="hoge-foo-bar"</p>'
    html += '<p>SKYPE_ID="-YOUR-SKYPE-ID-"</p>'
    html += 'curl --data-urlencode "name=${SKYPE_ID}" --data-urlencode "message=${MESSAGE}" -L -o /dev/null -s http://ec2-46-51-234-206.ap-northeast-1.compute.amazonaws.com/post/'
    html += '<hr>'
    html += '<h2>curl(STDIN)</h2>'
    html += 'echo "message=$MESSAGE" | curl --data @- --data-urlencode "name=${SKYPE_ID}" -L -o /dev/null -s http://ec2-46-51-234-206.ap-northeast-1.compute.amazonaws.com/post/'
    html += '<hr>'

    ## TODO : error...
    ## facebook like
    #html += '<center>'
    #html += '<div class="fb-like" data-send="false" data-width="450" data-show-faces="false"></div>'
    #html += '</center>'

    # twitter share
    html += '<center>'
    html += '<a href="https://twitter.com/share" class="twitter-share-button" data-url="http://bit.ly/skype-bot">Tweet</a> <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>' 
    html += '</center>'

    # @yuki777
    html += '<center><a href="https://twitter.com/yuki777">@yuki777</a></center>'
    html += '</body></html>'
    return html

@app.route("/post/", methods=['POST'])
def post():
    name = request.form['name']
    message = request.form['message']
    return redirect('/' + urllib.quote_plus(name) + '/' + urllib.quote_plus(message.encode('utf8')) + '/')

@app.route("/<name>/<path:message>/", methods=['GET'])
def message(name, message):
    message = urllib.unquote_plus(message.encode('utf8'))
    app.skype.SendMessage(name, message)

    log = time.asctime() + " " + name + "\n"
    f = open('/tmp/flask.skype.log', 'a')
    f.write(log)
    f.close()

    return '<html><body><a href="/">TOP</a></body></html>'

@app.route("/channel.html")
def channel():
    return '<script src="//connect.facebook.net/en_US/all.js"></script>'

if __name__ == "__main__":
    app.run(host="ec2-46-51-234-206.ap-northeast-1.compute.amazonaws.com", port=80)

