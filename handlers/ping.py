def ping_handler(app):
    @app.route('/ping', methods=['GET', 'POST', 'HEAD'])
    def ping():
        return 'pong', 200
