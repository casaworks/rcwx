#! /usr/bin/env python
# coding:utf-8

import xml.etree.ElementTree as ET
import time

def fromstring(string):
	xml = ET.fromstring(string)
	msg_type = xml.find('MsgType').text
	from_user = xml.find('FromUserName').text
	to_user = xml.find('ToUserName').text
	create_time = xml.find('CreateTime').text
	if msg_type == 'text':
		content = xml.find('Content').text
		msg = TextMessage(from_user, to_user, content, create_time)
	elif msg_type == 'image':
		pic_url = xml.find('PicUrl').text
		msg = ImageMessage(from_user, to_user, pic_url, create_time)
	elif msg_type == 'location':
		location_x = xml.find('Location_X').text
		location_y = xml.find('Location_Y').text
		scale = xml.find('Scale').text
		label = xml.find('Label').text
		msg = LocationMessage(from_user, to_user, location_x, location_y, scale, label,  create_time)
	elif msg_type == 'link':
		title = xml.find('Title').text
		description = xml.find('Description').text
		url = xml.find('Url').text
		msg = LinkMessage(from_user, to_user, title, description, url, create_time)
	elif msg_type == 'event':
		event = xml.find('Event').text
		event_key = xml.find('EventKey').text
		msg = EventMessage(from_user, to_user, event, event_key, create_time)
	else:
		raise MessageTypeError('can not parse message type %s.' % msg_type)
	return msg

class MessageTypeError(Exception):
	pass

class Message:
	def __init__(self, msg_type, from_user, to_user, create_time=None):
		self.msg_type = msg_type
		self.from_user = from_user
		self.to_user = to_user
		self.create_time = create_time if create_time else str(int(time.time()))
	
	def dump_header(self, xml):
		self.append_element('ToUserName', self.to_user, xml)
		self.append_element('FromUserName', self.from_user, xml)
		self.append_element('CreateTime', self.create_time, xml)
		self.append_element('MsgType', self.msg_type, xml)
	
	def append_element(self, name, value, xml):
		e = ET.Element(name)
		e.text = value
		xml.append(e)
		return e

class TextMessage(Message):
	def __init__(self, from_user, to_user, content, create_time=None, func_flag=0):
		Message.__init__(self, 'text', from_user, to_user, create_time)
		self.content = content
		self.func_flag = func_flag
	
	def dump(self):
		xml = ET.Element('xml')
		self.dump_header(xml)
		self.append_element('Content', self.content, xml)
		self.append_element('FuncFlag', self.func_flag, xml)
		return ET.tostring(xml, encoding='utf-8')

class ImageMessage(Message):
	def __init__(self, from_user, to_user, pic_url, create_time=None):
		Message.__init__(self, 'image', from_user, to_user, create_time)
		self.pic_url = pic_url

class LocationMessage(Message):
	def __init__(self, from_user, to_user, location_x, location_y, scale, label, create_time=None):
		Message.__init__(self, 'location', from_user, to_user, create_time)
		self.location_x = location_x
		self.location_y = location_y
		self.scale = scale
		self.label = label

class LinkMessage(Message):
	def __init__(self, from_user, to_user, title, description, url, create_time=None):
		Message.__init__(self, 'link', from_user, to_user, create_time)
		self.title = title
		self.description = description
		self.url = url

class EventMessage(Message):
	def __init__(self, from_user, to_user, event, event_key, create_time=None):
		Message.__init__(self, 'event', from_user, to_user, create_time)
		self.event = event
		self.event_key = event_key

class MusicMessage(Message):
	def __init__(self, from_user, to_user, title, music_url, hq_music_url, create_time=None, func_flag=0):
		Message.__init__(self, 'music', from_user, to_user, create_time)
		self.title = title
		self.music_url = music_url
		self.hq_music_url = hq_music_url
		self.func_flag = func_flag
	
	def dump(self):
		xml = ET.Element('xml')
		self.dump_header(xml)
		self.append_element('Title', self.title, xml)
		self.append_element('MusicUrl', self.music_url, xml)
		self.append_element('HQMusicUrl', self.hq_music_url, xml)
		self.append_element('FuncFlag', self.func_flag, xml)
		return ET.tostring(xml, encoding='utf-8')

class Article():
	def __init__(self, title, description, pic_url, url):
		self.title = title
		self.description = description
		self.pic_url = pic_url
		self.url = url
	
	def append_element(self, name, value, xml):
		e = ET.Element(name)
		e.text = value
		xml.append(e)
		return e
	
	def to_element(self):
		e = ET.Element('item')
		self.append_element('Title', self.title, e)
		self.append_element('Description', self.description, e)
		self.append_element('PicUrl', self.pic_url, e)
		self.append_element('Url', self.url, e)
		return e

class NewsMessage(Message):
	def __init__(self, from_user, to_user, articles=None, create_time=None, func_flag=0):
		Message.__init__(self, 'news', from_user, to_user, create_time)
		self.articles = articles if articles else []
		self.func_flag = func_flag
	
	def append_article(self, article):
		self.articles.append(article)
	
	def dump(self):
		xml = ET.Element('xml')
		self.dump_header(xml)
		self.append_element('ArticleCount', str(len(self.articles)), xml)
		articles_element = self.append_element('Articles', None, xml)
		for article in self.articles:
			article_element = article.to_element()
			articles_element.append(article_element)
		self.append_element('FuncFlag', self.func_flag, xml)
		return ET.tostring(xml, encoding='utf-8')

