from flask import request, jsonify
import uuid
from db import DB
from helpers import is_tg_access, client_version_check

def account_handlers(app, db):
    # Хендлер для аутентификации пользователя
    @app.route('/login', methods=['POST'])
    def login():
        name = request.form.get('name')
        password = request.form.get('password')

        if not name or not password:
            return jsonify(error='Отсутствует имя или пароль.'), 400

        if not db.check_user_password(name, password):
            return jsonify(error='Неверные имя или пароль.'), 401

        if is_tg_access():
            user_id = request.args.get('user_id')
            if not user_id:
                return jsonify(error='Отсутствует user_id.'), 422
            db.set_tg_user_id(name, int(user_id))
            return jsonify(status='ok'), 200

        result = client_version_check()
        if result:
        	return result

        user_token = str(uuid.uuid4())
        db.set_user_token(name, user_token)
        return jsonify(user_token=user_token), 200

    # Хендлер для регистрации пользователя
    @app.route('/reg', methods=['POST'])
    def register_user():
        name = request.form.get('name')
        password = request.form.get('password')
        print(name, password)

        if not name or not password:
            return jsonify(error='Отсутствует имя или пароль.'), 400

        if db.get_user(name):
            return jsonify(error='Имя пользователя уже занято.'), 409

        user_token = db.reg_user(name, password)
        return jsonify(user_token=user_token), 200