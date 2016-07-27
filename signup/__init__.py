from flask import Flask
from flask_sslify import SSLify

from signup import settings


static_folder = settings.get('STATIC_FOLDER')
app = Flask(__name__, static_folder=static_folder)
app.config.from_object(settings)
app.debug = app.config['DEBUG']

if app.config['SSLIFY']:
    sslify = SSLify(app, skips=['healthcheck'])  # noqa

from signup import routes  # noqa
