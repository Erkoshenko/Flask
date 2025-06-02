from flask import request, jsonify
from helpers import is_tg_access

def balance_handlers(app, db):
    @app.route('/get_balance', methods=['GET'])
    def _get_balance():
        if is_tg_access():
            user_id = request.args.get('user_id')
            if not user_id:
                return jsonify(error='Отсутвует user_id.'), 422

            user_data = db.get_user_by_tg_id(int(user_id))
            if not user_data:
                return jsonify(error='Нету пользователя под ваш тг айди.'), 404

            return jsonify(balance=str(user_data[3])), 200  # 3 — это индекс баланса

        user_name = request.args.get('name')
        if not user_name:
            return jsonify(error='Отсутвует user_name.'), 400

        balance = db.get_balance(user_name)
        if balance is None:
            return jsonify(error='Пользователя не существует.'), 404

        return jsonify(balance=balance), 200