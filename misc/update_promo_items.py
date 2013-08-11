#! /usr/bin/env python
# coding:utf-8

import cookielib
import urllib2
import urllib
import re
import os
from lxml import etree
from lxml.html.soupparser import fromstring
import mongotools
import pymongo
import codecs
import json

def response_encoding(response):
    content_type = response.info().getheader('Content-Type')
    return re.search(r"charset=([^']+)$", content_type).group(1)
    
def login(account, origin_password, password):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    
    res = opener.open("http://www.alimama.com/index.htm")
    html = res.read().decode(response_encoding(res))
    _tb_token_ = re.search(r"_tb_token_' type='hidden' value='([^']+)'", html).group(1)

    post_params = {}
    post_params['_tb_token_'] = _tb_token_
    post_params['style'] = ''
    post_params['redirect'] = ''
    post_params['proxy'] = 'http://www.alimama.com/proxy.htm'
    post_params['logname'] = account
    post_params['originalLogpasswd'] = origin_password
    post_params['logpasswd'] = password
    
    post_data = urllib.urlencode(post_params)
    req = urllib2.Request('http://www.alimama.com/member/minilogin_act.htm', post_data)
    opener.open(req)
    
    return opener
    
def decrypt_item_url(opener, encrypted_url):
    res = opener.open(encrypted_url)
    redirect_url = res.geturl()

    url = urllib.unquote(redirect_url[redirect_url.index('=') + 1:])

    req = urllib2.Request(url)
    req.add_header('Referer', redirect_url)
    res = opener.open(req)

    url = res.geturl()
    return url.replace('detail.tmall', 'item.taobao')
    
def get_promotion_url(opener, item_id, item_type):
    item_url = 'http://item.taobao.com/item.htm?id=' + item_id
    post_params = {
        'type': item_type,
        'promotionURL': item_url
    }
    req = urllib2.Request('http://u.alimama.com/union/spread/activities/linkTransTools.do', urllib.urlencode(post_params))
    res = opener.open(req)
    html = res.read().decode(response_encoding(res))
    return re.search(r'(http://s.click.taobao.com[^"]+)', html).group(1)

def parse_campaign_page(opener, campaign_id, omid, shopkeeper_id, shop_type, page):
    post_params = {}
    post_params['campaignID'] = campaign_id
    post_params['omid'] = omid
    post_params['shopkeeperID'] = shopkeeper_id
    post_params['toPage'] = str(page)
    post_params['od'] = '_totalnum'
    post_params['perPageSize'] = '40'
    post_data = urllib.urlencode(post_params)
    req = urllib2.Request('http://u.alimama.com/union/spread/selfservice/merchandiseDetail.htm', post_data)
    res = opener.open(req)
    html = res.read().decode(response_encoding(res))
    xml_root = fromstring(html)
    xml_items = xml_root.xpath("//div[@class='list-info']")
    items = []
    if xml_items:
        for xml_item in xml_items:
            xml_img = xml_item.xpath("a/img")[0]
            xml_a = xml_item.xpath("a")[1]
            xml_p = xml_item.xpath("p[@class='shopkeeper']")[0]
            item_image = xml_img.attrib['src']
            item_name = xml_a.text.strip()
            item_href = xml_a.attrib['href']
            item_id = re.search(r'id=(\d+)', item_href).group(1)
            item_shopkeeper = xml_p.text[3:].strip()
            item_price = float(xml_item.getparent().getnext().text[:-1])
            promo_url = decrypt_item_url(opener, get_promotion_url(opener, item_id, shop_type))
            item = {
                'id': item_id,
                'name': item_name,
                'price': item_price,
                'image': item_image,
                'shopkeeper': item_shopkeeper,
                'promo_url': promo_url
            }
            items.append(item)
            print 'add %s' % item_name
    return items

def parse_campaign(opener, campaign_id, omid, shopkeeper_id, shop_type):
    items = []
    for page in xrange(1, 1000):
        print 'parse page %d' % page
        page_items = parse_campaign_page(opener, campaign_id, omid, shopkeeper_id, shop_type, page)
        items.extend(page_items)
        if len(page_items) < 40:
            break
    return items
    
def main():
    opener = login('royalcanin@geekernel.com', 'cuijie1984', 'f7c5b7d9cf9e77ccdb580f3b51fbab87')    
    items = parse_campaign(opener, '0', '1728261286', '44627268', 'tmall')
    
    print 'dump items to promo_items.json'
    out = os.path.join(os.path.dirname(__file__), 'promo_items.json')
    with codecs.open(out, 'w', encoding='utf-8') as fp:
        json.dump(items, fp, ensure_ascii=False, indent=4, separators=(',', ': '))
        
    db = pymongo.MongoClient().royalcanin
    print 'dump items to mongodb'
    mongotools.update_collection(db, 'taobao_items', items)
     
if __name__ == '__main__':
    main()