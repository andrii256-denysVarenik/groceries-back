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
            tavriav.get_start({
                "corn": 96,
                "buckwheat": 94,
                "rice": 97,
                "barley": 102,
                "wheat": 100,
            })
            metro.get_start({
                "corn": "corn-groats",
                "buckwheat": "buckwheat",
                "rice": "rice",
                "barley": "barley-groats",
                "wheat": "wheat-groats",
            })
            auchan.get_start({
                "corn": "corn-groats",
                "buckwheat": "buckwheat",
                "rice": "rice",
                "barley": "barley-groats",
                "wheat": "wheat-groats",
            })
            fozzy.get_start({
                "corn": '300149-kukuruza',
                "buckwheat": '300143-krupa-grechnevaya',
                "rice": '300152-ris',
                "barley": '300148-krupa-yachnevaya',
                "wheat": '300147-krupa-pshenichnaya',
            })
        else:
            print('Exception')
            return render_template('config.html', img=True)
    return render_template('config.html')
