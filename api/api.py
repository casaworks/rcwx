# coding:utf-8

from flask import *
from flask import render_template
from weixin.app import App
import pymongo
import redis

app = Flask(__name__)
app.debug = True

wx_host = 'http://api.royalcanin.dev.geekernel.com' if app.debug else 'http://api.royalcanin.geekernel.com'
wx_token = 'geekernel'

mongo = pymongo.MongoClient()
db = mongo.royalcanin
redis_db = redis.Redis()
weixin_app = App(wx_host, wx_token, db, redis_db)

@app.route('/weixin', methods=['GET', 'POST'])
def weixin_service():
    return weixin_app.serve(app, 'geekernel')
    
@app.route('/catalog')
def show_catalog():
    cat_products = db.products.find({"$or": [{"cid": {"$in": ['20', '21', '22']}}, {"id": '86'}]})
    dog_products = db.products.find({"$or": [{"cid": {"$in": ['1', '2', '3', '4', '5', '6', '7']}}, {"id": '87'}]})
    cat_medi_products = db.products.find({"cid": '41'})
    dog_medi_products = db.products.find({"cid": '40'})
    categories = [
        {
            "name": u'猫主粮',
            "products": cat_products
        },
        {
            "name": u'犬主粮',
            "products": dog_products
        },
        {
            "name": u'猫处方粮',
            "products": cat_medi_products
        },
        {
            "name": u'犬处方粮',
            "products": dog_medi_products
        }
    ]
    return render_template('catalog.html', categories=categories)
    
@app.route('/product')
@app.route('/product/<product_id>')
def show_product(product_id=None):
    if not product_id:
        products = db.products.find()
        return render_template('products.html', products=products)
    product_ids = product_id.split(',')
    if len(product_ids) == 1:
        product = db.products.find_one({ "id": product_ids[0] })
        if product:
            taobao_items = db.taobao_items.find({"name": {"$regex": product['name']}})
            product['taobao_items'] = taobao_items
            return render_template('product.html', product=product)
        else:
            abort(404)
    else:
        products = []
        for product_id in product_ids:
            product = db.products.find_one({"id": product_id })
            if product:
                products.append(product)
        return render_template('products.html', products=products)
        
@app.route('/video')
@app.route('/video/<video_id>')
def show_videos(video_id=None):
    videos = db.videos.find({ 'id': video_id }) if video_id else db.videos.find()
    return render_template('video.html', videos=videos)

def main():
    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    main()
