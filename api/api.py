#! /usr/bin/env python
# coding:utf-8

from flask import * 
import json
import hashlib
import xml.etree.ElementTree as ET
import weixin

app = Flask(__name__)
app.debug = True

TOKEN = 'geekernel'

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
                response = weixin.TextMessage(msg.to_user, msg.from_user, u'欢迎关注').dump()
                return response
        elif msg.msg_type == 'text':
			response = weixin.TextMessage(msg.to_user, msg.from_user, msg.content).dump()
			app.logger.debug(response)
			return response

def main():
	app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
	main()
