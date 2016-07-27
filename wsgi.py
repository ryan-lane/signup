from signup import app


if __name__ == '__main__':
    app.run(
        host=('HOST', '127.0.0.1'),
        port=app.config.get('PORT', 8000),
        debug=app.config.get('DEBUG', True)
    )
