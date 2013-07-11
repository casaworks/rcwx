#! /usr/bin/env python

from flask import * 
import json
import hashlib

app = Flask(__name__)
app.debug = True

TOKEN = 'geekernel'

@app.route('/')
def hello():
	return "Hello, World!"

@app.route('/weixin/verify')
def verify():
	args = request.args
	signature = args['signature']
	timestamp = args['timestamp']
	nonce = args['nonce']
	echostr = args['echostr']
	a = (TOKEN, timestamp, nonce)
	a.sort()
	sha1 = hashlib.sha1()
	sha1.update(''.join(a))
	digest = sha1.digest()
	return ' '.join(TOKEN, timestamp, nonce, echostr, digest, signature)
	

def main():
	app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
	main()
