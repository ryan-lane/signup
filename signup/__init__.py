from logging.config import dictConfig

from flask import Flask
from flask_sslify import SSLify

from signup import settings


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default',
        'stream': 'ext://sys.stdout',
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

static_folder = settings.get('STATIC_FOLDER')
app = Flask(__name__, static_folder=static_folder)
app.config.from_object(settings)
app.debug = app.config['DEBUG']

if app.config['SSLIFY']:
    sslify = SSLify(app, skips=['healthcheck'])  # noqa

from signup import routes  # noqa
