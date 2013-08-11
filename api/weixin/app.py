# coding:utf-8

from flask import *
from message import *
from command import *
import os
import re
import redis
import hashlib
import urllib
import urllib2
import cookielib
import dianping
import xml.etree.ElementTree as ET
import json
import redis

CAT = u'猫咪'
DOG = u'狗狗'
        
class CatReqSelCommand(SelectionCommand):
    def __init__(self, app, desc, breed):
        SelectionCommand.__init__(self, app, desc, u'您的爱猫是否有以下特殊需求？')
        self.append_command(CatResultCommand(app, u'减肥', ['57']))
        self.append_command(CatResultCommand(app, u'挑嘴', ['53']))
        self.append_command(CatResultCommand(app, u'去除毛球', ['58']))
        self.append_command(CatResultCommand(app, u'去除牙结石', ['60']))
        self.append_command(CatResultCommand(app, u'亮泽毛发', ['59']))
        product_ids = ['47'] if breed == u'波斯猫' else ['48'] if breed == u'英国短毛猫' else ['51', '52', '54', '55']
        self.append_command(CatResultCommand(app, u'无特殊需求', product_ids))

class CatAgeSelectionCommand(SelectionCommand):
    def __init__(self, app, breed):
        SelectionCommand.__init__(self, app, breed, u'您猫咪的年龄区间是？')
        self.append_command(CatResultCommand(app, u'< 1月', u'您的小猫还在哺乳期，皇家推荐由其母乳喂养。'))
        self.append_command(CatResultCommand(app, u'1月 - 4月', ['46'] if breed == u'波斯猫' else ['86', '49']))
        self.append_command(CatResultCommand(app, u'4月 - 12月', ['46'] if breed == u'波斯猫' else ['50']))
        self.append_command(CatReqSelCommand(app, u'12月 - 10岁', breed))
        self.append_command(CatResultCommand(app, u'> 10岁', ['56']))

class CatBreedSelectionCommand(SelectionCommand):
    def __init__(self, app):
        SelectionCommand.__init__(self, app, CAT, u'您猫咪的品种是？')
        self.append_command(CatAgeSelectionCommand(app, u'波斯猫'))
        self.append_command(CatAgeSelectionCommand(app, u'英国短毛猫'))
        self.append_command(CatAgeSelectionCommand(app, u'其它'))
        
class ResultCommand(Command):
    def __init__(self, app, desc, type, product_ids):
        Command.__init__(self, app, desc)
        self.type = type
        self.product_ids = product_ids
        
    def prompt_help(self, msg):
        if isinstance(self.product_ids, list):
            return self.app.make_result_list(self.product_ids, msg, self.type)
        else:
            return TextMessage(msg.to_user, msg.from_user, self.product_ids)
            
    def respond_to_message(self, msg):
        self.app.quit2rootcmd(msg.from_user)
        return self.app.rootcmd.prompt_help(msg)
        
class DogResultCommand(ResultCommand):
    def __init__(self, app, desc, product_ids):
        ResultCommand.__init__(self, app, desc, DOG, product_ids)
        
class CatResultCommand(ResultCommand):
    def __init__(self, app, desc, product_ids):
        ResultCommand.__init__(self, app, desc, CAT, product_ids)
        
class DogAgeSelectionCommand(SelectionCommand):
    def __init__(self, app, breed):
        SelectionCommand.__init__(self, app, breed, u'您狗狗的年龄区间是？')
        if breed == u'贵宾':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['24', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 10月', ['1']))
            self.append_command(DogResultCommand(app, u'10月 - 8岁', ['6']))
            self.append_command(DogResultCommand(app, u'> 8岁', ['27']))
        elif breed == u'吉娃娃':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['87']))
            self.append_command(DogResultCommand(app, u'2月 - 8月', ['2']))
            self.append_command(DogResultCommand(app, u'8月 - 8岁', ['8']))
            self.append_command(DogResultCommand(app, u'> 8岁', ['23']))
        elif breed == u'金毛':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['36', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 15月', ['17']))
            self.append_command(DogResultCommand(app, u'> 15月', ['18']))
        elif breed == u'可卡':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['32', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 12月', ['33']))
            self.append_command(DogResultCommand(app, u'> 12月', ['5']))
        elif breed == u'拉布拉多':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['36', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 15月', ['15']))
            self.append_command(DogResultCommand(app, u'> 15月', ['16']))
        elif breed == u'迷你雪纳瑞':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['24', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 10月', ['25']))
            self.append_command(DogResultCommand(app, u'10月 - 8岁', ['7']))
            self.append_command(DogResultCommand(app, u'> 8岁', ['27', '31']))
        elif breed == u'西高地白梗':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['24', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 10月', ['25']))
            self.append_command(DogResultCommand(app, u'10月 - 8岁', ['4']))
            self.append_command(DogResultCommand(app, u'> 8岁', ['27', '32']))
        elif breed == u'约克夏':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['87']))
            self.append_command(DogResultCommand(app, u'2月 - 10月', ['3']))
            self.append_command(DogResultCommand(app, u'10月 - 8岁', ['9']))
            self.append_command(DogResultCommand(app, u'> 8岁', ['23']))
        elif breed == u'德国牧羊犬':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['36', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 15月', ['19']))
            self.append_command(DogResultCommand(app, u'> 15月', ['20']))
        elif breed == u'藏獒':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['40', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 8月', ['12']))
            self.append_command(DogResultCommand(app, u'8月 - 24月', ['13']))
            self.append_command(DogResultCommand(app, u'> 24月', ['14']))
        elif breed == u'迷你犬/4公斤以下':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['87']))
            self.append_command(DogResultCommand(app, u'2月 - 10月', ['21']))
            self.append_command(DogResultCommand(app, u'10月 - 8岁', ['22']))
            self.append_command(DogResultCommand(app, u'> 8岁', ['23']))
        elif breed == u'小型犬/10公斤以下':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['24', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 10月', ['25', '29']))
            self.append_command(DogResultCommand(app, u'10月 - 8岁', ['26', '30', '28']))
            self.append_command(DogResultCommand(app, u'> 8岁', ['27', '31']))
        elif breed == u'中型犬/11-25公斤':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['32', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 12月', ['33']))
            self.append_command(DogResultCommand(app, u'> 12月', ['34', '35']))
        elif breed == u'大型犬/26-44公斤':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['36', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 15月', ['37']))
            self.append_command(DogResultCommand(app, u'> 15月', ['38', '39']))
        else: # breed == u'巨型犬/45公斤以上':
            self.append_command(DogResultCommand(app, u'1月 - 2月', ['40', '87']))
            self.append_command(DogResultCommand(app, u'2月 - 8月', ['41']))
            self.append_command(DogResultCommand(app, u'8月 - 24月', ['42']))
            self.append_command(DogResultCommand(app, u'> 24月', u'对不起，没有符合您需求的产品。')) 
            
class DogOtherSelectionCommand(SelectionCommand):
    def __init__(self, app):
        SelectionCommand.__init__(self, app, u'其它', u'您爱犬成年后的体重是？')
        self.append_command(DogAgeSelectionCommand(app, u'迷你犬/4公斤以下'))
        self.append_command(DogAgeSelectionCommand(app, u'小型犬/10公斤以下'))
        self.append_command(DogAgeSelectionCommand(app, u'中型犬/11-25公斤'))
        self.append_command(DogAgeSelectionCommand(app, u'大型犬/26-44公斤'))
        self.append_command(DogAgeSelectionCommand(app, u'巨型犬/45公斤以上'))
        
class DogBreedSelectionCommand(SelectionCommand):
    def __init__(self, app):
        SelectionCommand.__init__(self, app, DOG, u'您狗狗的品种是？')
        self.append_command(DogAgeSelectionCommand(app, u'贵宾'))
        self.append_command(DogAgeSelectionCommand(app, u'吉娃娃'))
        self.append_command(DogAgeSelectionCommand(app, u'金毛'))
        self.append_command(DogAgeSelectionCommand(app, u'可卡'))
        self.append_command(DogAgeSelectionCommand(app, u'拉布拉多'))
        self.append_command(DogAgeSelectionCommand(app, u'迷你雪纳瑞'))
        self.append_command(DogAgeSelectionCommand(app, u'西高地白梗'))
        self.append_command(DogAgeSelectionCommand(app, u'约克夏'))
        self.append_command(DogAgeSelectionCommand(app, u'德国牧羊犬'))
        self.append_command(DogAgeSelectionCommand(app, u'藏獒'))
        self.append_command(DogOtherSelectionCommand(app))

class ProductSelectionCommand(SelectionCommand):
    def __init__(self, app):
        SelectionCommand.__init__(self, app, u'产品选购向导', u'您的爱宠是？')
        self.append_command(CatBreedSelectionCommand(app))
        self.append_command(DogBreedSelectionCommand(app))

class VerificationCommand(Command):
    def __init__(self, app):
        Command.__init__(self, app, u'真伪认证说明')
    
    def prompt_help(self, msg):
        self.app.quit2rootcmd(msg.from_user)
        return ImageTextMessage(msg.to_user, msg.from_user, u'真伪认证说明', u'请揭开产品包装上的标签，然后发送标签下的16位验证码。', self.app.url_for_image('product_verify.jpg'))
    
    def prompt_error(self, msg):
        return TextMessage(msg.to_user, msg.from_user, self.append_exit_prompt(u'验证码格式有误，请输入正确的16位验证码。'))
    
    def respond_to_message(self, msg):
        if isinstance(msg, TextMessage):
            match = re.match(r'(\d{4})\s*(\d{4})\s*(\d{4})\s*(\d{4})\s*', msg.content)
            if match:
                return self.respond_to_validation(msg, match.groups())

    def get_viewstate_eventvalidation(self, content):
        return re.findall(r'value="([^"]+)"', content)

    def respond_to_validation(self, msg, codes):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        post_values = {}
        post_values['ProcCodePart1'] = codes[0]
        post_values['ProcCodePart2'] = codes[1]
        post_values['ProcCodePart3'] = codes[2]
        post_values['ProcCodePart4'] = codes[3]
        post_values['__VIEWSTATE'] = '/wEPDwUJMTE1MTY4NzU1D2QWAmYPZBYEAgYPDxYCHgdWaXNpYmxlaGRkAggPDxYCHwBoZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgMFCE5leHRTdGVwBQVMb2dpbgUIUmVnaXN0ZXKaeSJXakopm5SIhmBH1SUtJ8BPcw=='
        post_values['__EVENTVALIDATION'] = '/wEWCAL774OqAgLVg/X8BgLYg/X8BgLXg/X8BgLSg/X8BgK8k6GGAgLvz/GACgK3tNX0DikTf6h0NPoTDAU9ctUpW66sA7MC'
        post_values['NextStep.x'] = 0
        post_values['NextStep.y'] = 0
        
        post_data = urllib.urlencode(post_values)       
        request = urllib2.Request('http://membership.royal-canin.cn/verifyc2.aspx', post_data)
        response = opener.open(request)
        final_url = response.geturl()
        codestr = ' '.join(codes)
        if final_url != 'http://membership.royal-canin.cn/verifyc3_1.aspx':
            verified_message = u'很遗憾，该产品验证码%s无法通过验证，请检查验证码是否输入错误。' % codestr
        else:
            html = opener.open(final_url).read().decode('utf-8')
            date_match = re.search(ur'(\d+)年(\d+)月(\d+)日(\d+)时', html)
            if date_match:
                date_parts = date_match.groups()
                verified_message = u'您所查询的验证码%s在%s年%s月%s日%s时已验证，如果此次验证并非您本人操作，请致电400-688-1527进行咨询。' % (codestr, date_parts[0], date_parts[1], date_parts[2], date_parts[3])
            else:
                verified_message = u'恭喜您，验证码%s成功通过验证，该产品为皇家正品！' % codestr
        return TextMessage(msg.to_user, msg.from_user, verified_message)
    
class QueryNearbyShopsCommand(Command):
    def __init__(self, app):
        Command.__init__(self, app, u'周边宠物店/医院')
        
    def prompt_help(self, msg):
        return ImageTextMessage(msg.to_user, msg.from_user, u'周边的宠物店/医院', u'请点击屏幕右下角的加号图标，然后点位置发送您的当前位置。', self.app.url_for_image('nearby_banner.jpg'))
        
    def respond_to_message(self, msg):
        if isinstance(msg, LocationMessage):
            return self.respond_to_location(msg)

    def respond_to_location(self, msg):
        lat = msg.location_x
        lng = msg.location_y
        shops = dianping.get_nearby_shops(lat, lng)
        if not shops:
            return TextMessage(msg.to_user, msg.from_user, u'呃...附近没有宠物店和宠物医院。')
        else:
            news = NewsMessage(msg.to_user, msg.from_user)
            title = Article(u'周边的宠物店/医院', None, self.app.url_for_image('nearby_banner.jpg'))
            news.append_article(title)
            for shop in shops:
                rating = shop['avg_rating']
                rating_mark = int(shop['avg_rating']) * u'\ue32f'
                if rating - int(rating) > 0.1:
                    rating_mark += u'\ue32e'
                title = u'%s\n%d点评  %d米' % (shop['name'] + rating_mark, shop['review_count'], shop['distance'])
                if u'宠物医院' in shop['categories']:
                    title = u'\ue13b ' + title
                article = Article(title, None, shop['s_photo_url'], shop['business_url'])
                news.append_article(article)
            return news
            
class CatalogCommand(Command):
    def __init__(self, app):
        Command.__init__(self, app, u'皇家产品家族')
        
    def catalog_url(self, category=None):
        return '%s/catalog#%s' % (self.app.host, category if category else '1')
        
    def prompt_help(self, msg):
        response = NewsMessage(msg.to_user, msg.from_user)
        response.append_article(Article(u'皇家产品家族', None, self.app.url_for_image('catalog_banner.jpg'), self.catalog_url()))
        response.append_article(Article(u'猫主粮', None, self.app.url_for_image('cat.png'), self.catalog_url('1')))
        response.append_article(Article(u'犬主粮', None, self.app.url_for_image('dog.png'), self.catalog_url('2')))
        response.append_article(Article(u'猫处方粮', None, self.app.url_for_image('cat_medi.png'), self.catalog_url('3')))
        response.append_article(Article(u'犬处方粮', None, self.app.url_for_image('dog_medi.png'), self.catalog_url('4')))
        self.app.quit2rootcmd(msg.from_user)
        return response
            
class RootCommand(SelectionCommand):
    def __init__(self, app):
        prompt = u'''\ue32f 回复产品关键字搜索产品，如“贵宾”，“小型犬 成犬”
\ue32f 回复当前位置搜索周边宠物店/医院
\ue32f 回复数字序号进入其它功能'''
        SelectionCommand.__init__(self, app, None, prompt)
        self.append_command(CatalogCommand(self.app))
        self.append_command(ProductSelectionCommand(self.app))
        # self.append_command(VerificationCommand(self.app))
        
    def make_prompt_text(self, key, text):
        return ' %s  %s' % (key, text)
        
    def respond_to_message(self, msg):
        if isinstance(msg, LocationMessage):
            return QueryNearbyShopsCommand(self.app).respond_to_message(msg)
        elif isinstance(msg, TextMessage):
            match = re.match(r'(\d{4})\s*(\d{4})\s*(\d{4})\s*(\d{4})\s*', msg.content)
            if match:
                return VerificationCommand(self.app).respond_to_message(msg)
            else:
                content = msg.content.strip()
                codes = self.get_command_codes()
                if not content in codes:
                    and_parts = []
                    keywords = content.split()
                    for keyword in keywords:
                        and_parts.append({"name": {"$regex": keyword}})
                    and_query_dict = {"$and": and_parts}
                    found_products = self.app.db.products.find(and_query_dict)
                    if found_products.count() > 0:
                        ids = []
                        for found_product in found_products:
                            ids.append(found_product['id'])
                        return self.app.make_result_list(ids, msg, None)
        return SelectionCommand.respond_to_message(self, msg)
        
class App:
    def __init__(self, host, token, db, redis_db, session_timeout=30):
        self.host = host
        self.token = token
        self.session_timeout = session_timeout
        self.rootcmd = None
        self.db = db
        self.products = self.db.products
        self.redis_db = redis_db
        
    def url_for_image(self, url):
        return '%s%s' % (self.host, url_for('static', filename=os.path.join('images', url)))
        
    def url_for_products(self, product_ids):
        url = '%s/product/' % self.host
        if isinstance(product_ids, list):
            url += ','.join(product_ids)
        else:
            url += product_ids
        return url
        
    def make_result_list(self, product_ids, msg, breed):
        articles = []
        for i, product_id in enumerate(product_ids):
            product = self.products.find_one({"id": product_id})
            product_html = self.url_for_products(product_id)
            if i == 8 and len(product_ids) > 9:
                article = Article(u'更多', None, None, self.url_for_products(product_ids))
                articles.append(article)
                break
            else:
                article = Article(product['name'], None, self.url_for_image(product['image']), self.url_for_products(product_id))
                articles.append(article)
        banner_image = self.url_for_image('cat_banner.jpg' if breed == CAT else 'dog_banner.jpg' if breed == DOG else 'catalog_banner.jpg')
        title_article = Article(u'发现%d款产品' % len(product_ids), None, banner_image, self.url_for_products(product_ids))
        articles.insert(0, title_article)
        return NewsMessage(msg.to_user, msg.from_user, articles)
        
    def get_root_command(self):
        if not self.rootcmd:
            self.rootcmd = RootCommand(self)
        return self.rootcmd
        
    def is_root_command(self, cmd):
        return self.rootcmd == cmd
    
    def route_command(self, cmd, routes):
        return self.route_command(cmd.get_command(routes[0]), routes[1:]) if routes else cmd
        
    def user_key(self, userid, keytype):
        return '%s:%s' % (userid, keytype)
        
    def user_route_key(self, userid):
        return self.user_key(userid, 'cmdpath')
        
    def reset_timeout(self, userid):
        self.redis_db.expire(self.user_route_key(userid), self.session_timeout)
        
    def enter_command(self, userid, cmdindex):
        self.redis_db.rpush(self.user_route_key(userid), cmdindex)
        self.reset_timeout(userid)
        
    def quit_command(self, userid):
        self.redis_db.rpop(self.user_route_key(userid))
        self.reset_timeout(userid)
        
    def quit2rootcmd(self, userid):
        self.redis_db.delete(self.user_route_key(userid))
        
    def get_user_routes(self, userid):
        return [int(route) for route in self.redis_db.lrange(self.user_route_key(userid), 0, -1)]
        
    def get_user_curcmd(self, userid):
        return self.route_command(self.get_root_command(), self.get_user_routes(userid))
    
    def serve(self, flask_app, token):
        if request.method == 'GET':
            args = request.args
            signature = args['signature']
            timestamp = args['timestamp']
            nonce = args['nonce']
            echostr = args['echostr']
            raw = ''.join(sorted([token, timestamp, nonce]))
            digest = hashlib.sha1(raw).hexdigest()
            if digest == signature:
                return echostr
            else:
                abort(401)
        else:
            data = request.data
            flask_app.logger.debug(data)
            msg = fromstring(data)
            response = self.route_command(self.get_root_command(), self.get_user_routes(msg.from_user)).respond_to(msg)
            if isinstance(msg, EventMessage) and msg.event == 'subscribe':
                response.content = u'“为您所爱，定制关爱”\n欢迎关注皇家宠物食品！\n' + response.content
            return response.dump()

    