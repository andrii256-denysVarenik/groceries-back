from datetime import date, datetime, time

from app import app
from flask_pymongo import PyMongo

dbClient = PyMongo(app)
db = dbClient.db['tavriav']


def insert_goods(data: dict) -> bool:
    return db[data["type"]].insert_one(data).acknowledged


def find_goods(type_good: str):
    return db[type_good].find({"date": datetime.combine(date.today(), time.min)})


def find_cheaper(type_good: str, d: datetime):
    try:
        return db[type_good].find({"date": d}).sort([("pricePerKg", 1)])[0]
    except:
        return
