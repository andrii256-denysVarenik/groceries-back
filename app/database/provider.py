from datetime import date, datetime, time

from app import app
from flask_pymongo import PyMongo


class DbProvider(object):

    def __init__(self):
        self.__dbClient = PyMongo(app)
        self._db = self.__dbClient.db['tavriav']

    def insert_goods(self, data: dict) -> bool:
        return self._db[data["type"]].insert_one(data).acknowledged

    def find_cheaper(self, type_good: str, d: datetime):
        try:
            return self._db[type_good].find({"date": d}).sort([("pricePerKg", 1)])[0]
        except:
            return

    def find_goods(self, type_good: str, args: dict):
        lim = 0

        query = {
            "date": datetime.combine(date.today(), time.min),
        }
        if 'price' in args:
            price = self.__price_filter(args["price"])
            if price:
                query.update(price)
        if 'shops' in args:
            shop = self.__shop_filter(args["shops"])
            if shop:
                query.update(shop)
        goods = self._db[type_good].find(query)

        if 'limit' in args:
            lim = self.__limit_filter(args["limit"])
        if 'filter' in args:
            if args['filter'] == 'cheaper':
                return goods.sort([("pricePerKg", 1)]).limit(lim)
            elif args['filter'] == 'expensive':
                return goods.sort([("pricePerKg", -1)]).limit(lim)
        return goods.limit(lim)

    @staticmethod
    def __price_filter(price: str):
        try:
            min_num, max_num = price.split('-')
            min_num, max_num = int(min_num), int(max_num)
            return {"pricePerKg": {
                "$gte": min_num,
                "$lte": max_num
            }}
        except:
            return False

    @staticmethod
    def __shop_filter(shop: str):
        return {"shopName": {'$nin': shop.split(',')}}

    @staticmethod
    def __limit_filter(limit: str):
        try:
            return int(limit)
        except:
            return 0
