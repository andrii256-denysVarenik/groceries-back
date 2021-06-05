from os import path, environ
BASE_DIR = path.abspath(path.dirname(__file__))


def get_mongo_uri() -> str:
    with open('mongo.txt', 'r', encoding='utf-8') as f:
        return f.readline()


class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY") or 'grocceris'
    DEBUG = environ.get('DEBUG') or True
    MONGO_URI = environ.get('MONGO') or get_mongo_uri()
