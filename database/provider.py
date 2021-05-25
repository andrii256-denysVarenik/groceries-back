from datetime import date, datetime, time

from pymongo import MongoClient

dbClient = MongoClient(host='127.0.0.1', port=27017)
db = dbClient["groceries"]


def insert_goods(data: dict) -> None:
    db[data["type"]].insert_one(data)


def find_goods(type_good: str):
    return db[type_good].find({"date": datetime.combine(date.today(), time.min)})


def find_cheaper(type_good: str, d: datetime):
    try:
        return db[type_good].find({"date": d}).sort([("pricePerKg", 1)])[0]
    except:
        return
