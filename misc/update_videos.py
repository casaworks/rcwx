#! /usr/bin/env python
# coding:utf-8

import urllib2
import re
import os
from lxml import etree
from lxml.html.soupparser import fromstring
import mongotools
import pymongo
import codecs
import json

VIDEOS_INDEX_URL = 'http://i.youku.com/u/UNjI3MzE2MDM2/videos'
VIDEO_URL_FORMAT = 'http://player.youku.com/embed/%s'

def response_encoding(response):
    content_type = response.info().getheader('Content-Type')
    return re.search(r"charset=([^']+)$", content_type).group(1)
    
def main():
    req = urllib2.Request(VIDEOS_INDEX_URL)
    res = urllib2.urlopen(req)
    html = res.read().decode(response_encoding(res))
    
    xml_root = fromstring(html)
    xml_items = xml_root.xpath("//div[@class='items']/ul[@class='v']")
    items = []
    
    if xml_items:
        for xml_item in xml_items:
            xml_img = xml_item.xpath("li[@class='v_thumb']/img")[0]
            item_image = xml_img.attrib['src']
            xml_title = xml_item.xpath("li[@class='v_title']/a")[0]
            item_href = xml_title.attrib['href']
            item_id = re.search(r'id_(.*)\.html', item_href).group(1)
            item_url = VIDEO_URL_FORMAT % item_id
            item_title = xml_title.text
            item_pub = xml_item.xpath("li[@class='v_pub']/span")[0].text
            xml_num = xml_item.xpath("li[@class='v_stat']/span[@class='num']")[0].text
            item_num = int(xml_num.replace(',', ''))
            item_length = xml_item.xpath("li[@class='v_time']/span[@class='num']")[0].text
            
            item = {
                'id' : item_id,
                'title': item_title,
                'image': item_image,
                'url': item_url,
                'length': item_length,
                'played_times': item_num
            }
            if item['id'] == 'XNTgyMDkyNTg4':
                continue
            if not next(iter([i for i in items if i['title'] == item['title']]), None):
                items.append(item)
        
    db = pymongo.MongoClient().royalcanin
    print 'dump items to mongodb'
    mongotools.update_collection(db, 'videos', items)
     
if __name__ == '__main__':
    main()