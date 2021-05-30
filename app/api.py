from app import app
from flask import render_template, jsonify, request
from datetime import date, timedelta, datetime, time
from app.database.provider import find_goods, find_cheaper
from hashlib import md5
from app.parser import get_start


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if md5(request.form.get('password').encode()).hexdigest() == '8a5da52ed126447d359e70c05721a8aa':
            get_start()
        else:
            print('Exception')
            return render_template('index.html', img=True)
    return render_template('index.html')


@app.route('/<string:type_good>/', methods=["GET"])
def goods(type_good):
    data = [good for good in find_goods(type_good)]
    for good in data:
        good["_id"] = str(good["_id"])
    return jsonify(data)


@app.route('/history/<string:type_good>/', methods=["GET"])
def history(type_good):
    dates = [date.today() - timedelta(days=i) for i in range(0, 31)]
    dates = [datetime.combine(d, time.min) for d in dates]
    history = []
    for d in dates:
        min_price = find_cheaper(type_good, d)
        if min_price:
            history.append({"date": min_price["date"], "price": min_price["pricePerKg"]})
    return jsonify(history)


@app.route('/cheaper/<string:type_good>/', methods=["GET"])
def cheaper(type_good):
    d = datetime.combine(date.today(), time.min)
    min_price = find_cheaper(type_good, d)
    return {"href": min_price["link"], "price": min_price["pricePerKg"]}
