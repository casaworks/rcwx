#! /usr/bin/env python
# coding:utf-8

import json
from os import path
import re
import codecs

def extract_code(name):
    match = re.search(ur'[a-zA-Z]+\d+', name)
    return match.group() if match else None

def make_sample_code_name_mapping(promo_items_json_file):
    with open(promo_items_json_file) as fp:
        promo_items = json.load(fp, 'utf-8')
        name_code_map = {}
        for promo_item in promo_items:
            name = promo_item['name']
            code = extract_code(name)
            if not code:
                continue
            name_code_map[name] = code
        return name_code_map
        
def get_most_similar_name(name, names):
    return next((i for i in names if i.find(name) != -1), None)
    
def append(data_json_file, promo_items_json_file):
    name_code_map = make_sample_code_name_mapping(promo_items_json_file)
    names = name_code_map.keys()
    with open(data_json_file) as fp:
        products = json.load(fp, encoding='utf-8')
        codes = []
        for product in products:
            cid = product['cid']
            name = product['name']
            most_similar_name = get_most_similar_name(name, names)
            if not most_similar_name:
                code = ''
                print 'cannot find code for %s' % name
            else:
                code = name_code_map[most_similar_name]
                if name == u'贵宾幼犬粮':
                    code = 'PD33'
                if code in codes:
                    print 'warning!!!!!!!!!!!!!!!!!'
                else:
                    codes.append(code)
                print '%s <-> %s: %s' % (name, code, most_similar_name)
            product['code'] = code
            
    with codecs.open(data_json_file, 'w', encoding='utf-8') as fp:
        json.dump(products, fp, ensure_ascii=False, indent=4, separators=(',', ': '))

def main():
    basedir = path.dirname(__file__)
    data_json_file = path.join(basedir, 'data.json')
    promo_items_json_file = path.join(basedir, 'sample_promo_items.json')
    append(data_json_file, promo_items_json_file)

if __name__ == '__main__':
    main()