from datetime import date, datetime, time

from app import app
from flask_pymongo import PyMongo

dbClient = PyMongo(app)
db = dbClient.db['tavriav']


def insert_goods(data: dict) -> bool:
    return db[data["type"]].insert_one(data).acknowledged


def find_goods(type_good: str, args: dict):
    query = {
        "date": datetime.combine(date.today(), time.min),
    }
    if "price" in args:
        nums = get_int_price(args['price'])
        if nums:
            query.update({"pricePerKg": {
                "$gte": nums[0],
                "$lte": nums[1]
            }})
    if 'shop' in args:
        shops = args['shop'].split(',')
        query.update({"shopName": {'$nin': shops}})

    goods = db[type_good].find(query)
    if 'filter' in args:
        if args['filter'] == 'cheaper':
            return goods.sort([("pricePerKg", 1)])
        elif args['filter'] == 'expensive':
            return goods.sort([("pricePerKg", -1)])
    return goods


def find_cheaper(type_good: str, d: datetime):
    try:
        return db[type_good].find({"date": d}).sort([("pricePerKg", 1)])[0]
    except:
        return


def get_int_price(price: str):
    try:
        min_num, max_num = price.split('-')
        return [int(min_num), int(max_num)]
    except:
        return False
