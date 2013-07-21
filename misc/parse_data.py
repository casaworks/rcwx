#! /usr/bin/env python
# coding:utf8

from lxml import etree
from lxml.html.soupparser import parse
import json
import sys
import os
import codecs
import re
import hashlib

base_dir = os.path.dirname(__file__)

def norm_spec(spec_text):
    spec_text = spec_text.lower()
    if spec_text.find('kg') != -1:
        return float(spec_text.rstrip('kg'))
    elif spec_text.find('g') != -1:
        return float(spec_text.rstrip('g')) / 1000
    else:
        return float(spec_text)
        
def norm_image_url(offical_url):
    basepath, ext = os.path.splitext(offical_url)
    norm_name = hashlib.md5(basepath).hexdigest()
    norm_url = norm_name + ext
    return norm_url
        
def parse_detail(id, cid, name, xml_product_content):
    if cid == '40' or cid == '41':
        text_content = xml_product_content.xpath("//p[@class='newtw']/following-sibling::p")[0].text_content().strip()
        text_lines = text_content.split()
        text_lines = [i.strip() for i in text_lines if i.strip()]
        detail = {}
        app = {}
        app['yes'] = app['no'] = ''
        for i, line in enumerate(text_lines):
            if line.startswith(u'适宜对象'):
                app['yes'] = line.lstrip(u'适宜对象')
            elif line.startswith(u'不适宜对象'):
                text = line.lstrip(u'不适宜对象').strip()
                if not text:
                    text = text_lines[i + 1]
                if text != u'无':
                    app['no'] = text
        detail['applicable'] = app
        features = [] 
        xml_features = xml_product_content.xpath("//div[@class='pl_detail']//td")
        for xml_feature in xml_features:
            xml_img = xml_feature.xpath("img")
            if not xml_img:
                xml_img = xml_feature.xpath("p/img")
            if xml_img:
                feature = {}
                feature['image'] = norm_image_url(xml_img[0].attrib['src'].strip())
                feature['desc'] = xml_feature.text_content().strip()
                features.append(feature)
        detail['features'] = features
    else:
        features = []
        title = xml_product_content.xpath("//p[@class='newtw']/b")[0].text
        desc = xml_product_content.xpath("//p[@class='newtw']/text()")[0].strip()
        feature = {}
        feature['title'] = title
        feature['desc'] = desc
        features.append(feature)
        if cid != '22':
            text_content = xml_product_content.xpath("//div[@class='pl_detail']")[0].text_content().strip()
            text_lines = text_content.split('\n')
            text_lines = [i.strip() for i in text_lines if i.strip()]
            for i, line in enumerate(text_lines[0::2]):
                feature = {}
                feature['title'] = line
                feature['desc'] = text_lines[2 * i + 1]
                features.append(feature)
        detail = {}
        detail['features'] = features
    return detail

def parse_product(id, cid, name):
    root = parse(os.path.join(base_dir, 'htmls', '%s.html' % id))
    xml_product_content = root.xpath("//div[@class='productContent']")[0]
    product_img = norm_image_url(xml_product_content.xpath("//img[@class='productPic']")[0].attrib['src'])
    product_name = xml_product_content.xpath("//p[@class='d_title']/span")[0].text
    product_for = xml_product_content.xpath("//p[@class='d_title']/label")[0].text.rstrip(u'。').strip()
    product_spec_texts = re.compile(u'/|／').split(xml_product_content.xpath("//p[@class='d_title']/text()")[1].strip()[3:])
    product_specs = [norm_spec(i) for i in product_spec_texts]
    xml_product_detail = xml_product_content.xpath("//div[@class='pl_detail']")[0]
    product_detail = parse_detail(id, cid, name, xml_product_content)
    product = {}
    product['id'] = id
    product['cid'] = cid
    product['name'] = product_name
    product['image'] = product_img
    product['for'] = product_for
    product['specs'] = product_specs
    product['detail'] = product_detail
    return product

def main():
    products = []
    for line in codecs.open(os.path.join(base_dir, 'product.lst'), encoding='utf8'):
        parts = line.strip().split(':')
        product = parse_product(parts[0], parts[1], parts[2])
        products.append(product)
    with codecs.open(os.path.join(base_dir, 'data.json'), 'w', encoding='utf8') as fp:
        json.dump(products, fp, ensure_ascii=False, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    main()


