from os import path, environ
BASE_DIR = path.abspath(path.dirname(__file__))


class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY") or 'grocceris'
    DEBUG = environ.get('DEBUG') or True
