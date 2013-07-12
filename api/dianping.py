#! /usr/bin/env python
# coding:utf-8

import urllib
import hashlib

appkey = '0193710644'
secret = 'b9f1abeb08f5492bb7d0ed4a40086929'
path = 'http://api.dianping.com/v1/business/find_businesses'

params_map = {}
params_map['latitude'] = '31.218173'
params_map['longitude'] = '121.415695'
params_map['sort'] = '7'
params_map['category'] = '宠物'

keys = sorted(params_map.keys())
params_list = []
for key in keys:
	params_list.append(key + params_map[key])

raw = appkey + ''.join(params_list) + secret
sign = hashlib.sha1(raw).hexdigest().upper()

params_map['appkey'] = appkey
params_map['sign'] = sign

url = '?'.join([path, urllib.urlencode(params_map)])
print url

response = urllib.urlopen(url)
print response.read()
