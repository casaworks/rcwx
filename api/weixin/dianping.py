#! /usr/bin/env python
# coding:utf-8

import urllib
import hashlib
import json

appkey = '0193710644'
secret = 'b9f1abeb08f5492bb7d0ed4a40086929'

def get_nearby_shops(lat, lng):
    path = 'http://api.dianping.com/v1/business/find_businesses'
    params_map = {}
    params_map['latitude'] = str(lat)
    params_map['longitude'] = str(lng)
    params_map['sort'] = '7'
    params_map['category'] = '宠物'
    params_map['limit'] = '9'
    params_map['sort'] = '7'
    params_map['offset_type'] = '1'
    params_map['radius'] = '5000'

    keys = sorted(params_map.keys())
    params_list = []
    for key in keys:
    	params_list.append(key + params_map[key])

    raw = appkey + ''.join(params_list) + secret
    sign = hashlib.sha1(raw).hexdigest().upper()

    params_map['appkey'] = appkey
    params_map['sign'] = sign

    url = '?'.join([path, urllib.urlencode(params_map)])

    response = urllib.urlopen(url)
    response_content = response.read()
    #print response_content
    
    shops = json.loads(response_content, 'utf8')['businesses']
    return shops

if __name__ == '__main__':
    print json.dumps(get_nearby_shops(31.21524, 121.420033), indent=4, ensure_ascii=False, encoding='utf-8')
