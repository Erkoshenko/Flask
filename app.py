from flask import Flask
#from config import Config
from db import DB
from handlers import register_handlers

app = Flask(__name__)
#app.config.from_object(Config)

db = DB()

# Регистрация хендлеров
register_handlers(app, db)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
