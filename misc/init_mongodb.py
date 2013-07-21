#! /usr/bin/env python
# coding:utf-8

import pymongo
import json
from os import path

def add_collection(db, collection_name, filename):
    collection = db[collection_name]
    collection.drop()
    jsonfile = path.join(path.dirname(__file__), filename)
    with open(jsonfile) as fp:
        values = json.load(fp, encoding='utf-8')
        for value in values:
            collection.save(value)

def main():
    mongo = pymongo.MongoClient()
    db = mongo.royalcanin
    add_collection(db, 'products', 'data.json')
    add_collection(db, 'taobao_items', 'promo_items.json')
    
def search_taobao_items(collection, keyword):
    return collection.find({'name': {'$regex': '.*%s.*' % keyword }})

if __name__ == '__main__':
    main()