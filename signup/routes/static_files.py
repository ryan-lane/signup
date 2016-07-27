import os

from signup import app
from signup.cache_control import no_cache


@app.route('/')
@no_cache
def index():
    response = app.send_static_file('index.html')
    return response


@app.route('/healthcheck')
def healthcheck():
    return '', 200


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/404.html')
def not_found():
    return app.send_static_file('404.html')


@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')


@app.route('/bower_components/<path:path>')
def components(path):
    return app.send_static_file(os.path.join('bower_components', path))


@app.route('/views/<path:path>')
def views(path):
    return app.send_static_file(os.path.join('views', path))


@app.route('/images/<path:path>')
def images(path):
    return app.send_static_file(os.path.join('images', path))


@app.route('/modules/<path:path>')
def modules(path):
    return app.send_static_file(os.path.join('modules', path))


@app.route('/styles/<path:path>')
def styles(path):
    return app.send_static_file(os.path.join('styles', path))
