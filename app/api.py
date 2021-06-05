from app import app
from flask import jsonify, request
from datetime import date, timedelta, datetime, time
from app.database.provider import DbProvider

db = DbProvider()


@app.route('/<string:type_good>/', methods=["GET"])
def goods(type_good):
    data = [good for good in db.find_goods(type_good, request.args.to_dict())]
    for good in data:
        good["_id"] = str(good["_id"])
    return jsonify(data)


@app.route('/history/<string:type_good>/', methods=["GET"])
def history(type_good):
    dates = [date.today() - timedelta(days=i) for i in range(0, 31)]
    dates = [datetime.combine(d, time.min) for d in dates]
    history = []
    for d in dates:
        min_price = db.find_cheaper(type_good, d)
        if min_price:
            history.append({"date": min_price["date"], "price": min_price["pricePerKg"]})
    return jsonify(history)
