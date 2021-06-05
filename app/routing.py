from app import app
from flask import request, render_template
from hashlib import md5
from app.parser import tavriav, metro, auchan, fozzy


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/api/groceries/v3.0/config/', methods=["GET", "POST"])
def config():
    if request.method == "POST":
        if md5(request.form.get('password').encode()).hexdigest() == '8a5da52ed126447d359e70c05721a8aa':
            tavriav.get_start()
            metro.get_start()
            auchan.get_start()
            fozzy.get_start()
        else:
            print('Exception')
            return render_template('config.html', img=True)
    return render_template('config.html')
