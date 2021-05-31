from app import app
from flask import request, render_template
from hashlib import md5
from app.parser.tavriav import get_start


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if md5(request.form.get('password').encode()).hexdigest() == '8a5da52ed126447d359e70c05721a8aa':
            get_start()
        else:
            print('Exception')
            return render_template('index.html', img=True)
    return render_template('index.html')