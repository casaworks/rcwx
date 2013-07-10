#! /usr/bin/env python

from flask import * 
import json

app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello, World!"

@app.route('/test/<value>')
def test(value):
	return value

def main():
	app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
	main()
