#! /usr/bin/env python
# coding:utf-8

from flask import * 
import json
import hashlib
import xml.etree.ElementTree as ET
import weixin
import re
import urllib
import urllib2
import dianping

app = Flask(__name__)
app.debug = True

TOKEN = 'geekernel'

GUIDE_MESSAGE = u'''欢迎关注皇家宠物食品！
输入序号:
1: 产品选购向导
2: 产品真伪验证
3: 周边的宠物店/医院
0: 查看帮助'''

HOST = 'http://58.246.240.122'

@app.route('/weixin', methods=['GET', 'POST'])
def weixin_service():
    if request.method == 'GET':
        args = request.args
        signature = args['signature']
        timestamp = args['timestamp']
        nonce = args['nonce']
        echostr = args['echostr']
        a = sorted([TOKEN, timestamp, nonce])
        raw = ''.join(a)
        app.logger.debug(raw)
        digest = hashlib.sha1(raw).hexdigest()
        if digest == signature:
            return echostr
        else:
            abort(401)
    else:
        data = request.data
        app.logger.debug(data)
        msg = weixin.fromstring(data)
        
        if msg.msg_type == 'event':
            if msg.event == 'subscribe':
                response = weixin.TextMessage(msg.to_user, msg.from_user, GUIDE_MESSAGE)
                return response.dump()
        elif msg.msg_type == 'text':
            content = msg.content.strip()
            if content == '2':
                response = weixin.NewsMessage(msg.to_user, msg.from_user)
                pic_url = '%s%s' % (HOST, url_for('static', filename='product_verify.png'))
                print pic_url
                article = weixin.Article(u'产品验证', u'揭开产品包装上的标签，发送标签下16位验证码', pic_url, None)
                response.append_article(article)
                return response.dump()
            if content == '0':
                response = weixin.TextMessage(msg.to_user, msg.from_user, GUIDE_MESSAGE)
                return response.dump()
            pattern = re.compile(r'(\d{4})\s*(\d{4})\s*(\d{4})\s*(\d{4})\s*')
            match = pattern.match(content)
            if match:
                response = respond_to_validation(msg, match.groups())
                return response.dump()
        elif msg.msg_type == 'location':
            response = respond_to_location(msg)
            #print response.dump()
            return response.dump()

def get_viewstate_eventvalidation(content):
    return re.findall(r'value="([^"]+)"', content)

def get_verified_url(code):
    return 'http://membership.royal-canin.cn/verifyc3_%d.aspx' % code

def get_verified_text(url):
    print url
    if url == get_verified_url(1):
        return u'您所查询的验证码之前已验证且使用，如果此次验证并非您本人操作，请致电400-688-1527进行咨询。'
    elif url == get_verified_url(2):
        return u'恭喜您，该产品为正品！'
    else:
        return u'很遗憾，该产品无法通过验证，请检查验证码是否输入错误。' 

def respond_to_validation(msg, codes):
    url = 'http://membership.royal-canin.cn/verifyc2.aspx'

    get_content = urllib2.urlopen(url).read()
    viewstate_eventvalidation = get_viewstate_eventvalidation(get_content)

    post_values = {}
    post_values['ProcCodePart1'] = codes[0]
    post_values['ProcCodePart2'] = codes[1]
    post_values['ProcCodePart3'] = codes[2]
    post_values['ProcCodePart4'] = codes[3]
    post_values['__VIEWSTATE'] = viewstate_eventvalidation[0] 
    post_values['__EVENTVALIDATION'] = viewstate_eventvalidation[1]
    post_values['NextStep.x'] = 0
    post_values['NextStep.y'] = 0
    post_data = urllib.urlencode(post_values)       
    request = urllib2.Request(url, post_data)
    response = urllib2.urlopen(request)
    status = response.getcode()
    #html = response.read();
    verified_message = get_verified_text(response.geturl())
    return weixin.TextMessage(msg.to_user, msg.from_user, verified_message)

def respond_to_location(msg):
    lat = msg.location_x
    lng = msg.location_y
    shops = dianping.get_nearby_shops(lat, lng)
    
    if not shops:
        return weixin.TextMessage(msg.to_user, msg.from_user, u'呃...附近没有宠物店和宠物医院。')
    else:
        news = weixin.NewsMessage(msg.to_user, msg.from_user)
        articles = []
        for shop in shops:
            title = u'%s\n%.1f分  %d点评  %d米' % (shop['name'], shop['avg_rating'], shop['review_count'], shop['distance'])
            article = weixin.Article(title, None, shop['s_photo_url'], shop['business_url'])
            news.append_article(article)
        return news

def main():
    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    main()
