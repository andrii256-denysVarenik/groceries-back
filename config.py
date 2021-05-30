from os import path, environ
BASE_DIR = path.abspath(path.dirname(__file__))


class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY") or 'grocceris'
    DEBUG = environ.get('DEBUG') or True
    MONGO_URI = "mongodb+srv://adrii-den:n7GylHu2Yi2dvBwk@groceries.0eojr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
