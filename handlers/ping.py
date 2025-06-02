def ping_handler(app):
    @app.route('/ping')
    def ping():
        return 'pong', 200
