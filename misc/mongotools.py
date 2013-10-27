#! /usr/bin/env python
# coding:utf-8

import pymongo
import json
from os import path

def update_collection_from_json(db, collection_name, jsonfile):
    with open(jsonfile) as fp:
        values = json.load(fp, encoding='utf-8')
        update_collection(db, collection_name, values)

def update_collection(db, collection_name, values):
    collection = db[collection_name]
    collection.drop()
    for value in values:
        collection.save(value)

def main():
    db = pymongo.MongoClient().royalcanin
    update_collection_from_json(db, 'products', 'data.json')
    update_collection_from_json(db, 'taobao_items', 'promo_items.json')

if __name__ == '__main__':
    main()