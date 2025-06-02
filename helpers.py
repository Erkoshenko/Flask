from flask import request, jsonify
from config import Config

def is_tg_access():
    """Проверка на доступ по Telegram API."""
    return request.headers.get("Authorization") == f"Bearer {Config.TG_ACCESS_TOKEN}"

def client_version_check():
    """Проверка версии клиента."""
    token = request.form.get('client_token')
    if token != Config.CLIENT_VERSION_TOKEN:
        return jsonify(error='Старая версия клиента.'), 400