from flask import request, jsonify
from helpers import client_version_check  # не забудь импортировать

def update_handlers(app, db):
    @app.route('/update', methods=['POST'])
    def _update():
        result = client_version_check()  # проверка версии клиента
        if result:
        	return result

        name = request.form.get('name')
        balance = request.form.get('balance')
        user_token = request.form.get('user_token')

        if not name or not balance or not balance.isdigit():
            return jsonify(error='Отсутствует имя или пароль.'), 400

        user_data = db.get_user(name)
        if not user_data:
            return jsonify(error="Пользователь не найден."), 404
        
        # name, password, tg_user_id, balance, token 
        _, _, _, db_balance, db_token = user_data

        if db_token != user_token:
            return jsonify(error='В аккаунт зашёл второй игрок.'), 401

        if abs(int(balance) - db_balance) > 25:
            return jsonify(error='Подозрения в использовании автокликера.'), 403

        db.update_balance(name, int(balance))
        return jsonify(status='ok'), 200