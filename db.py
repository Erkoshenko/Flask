import sqlite3
import uuid

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        """Инициализация БД"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                tg_user_id INTEGER,
                balance INTEGER DEFAULT 0,
                token TEXT NOT NULL,
                PRIMARY KEY (name)
            )
        """)
        self.conn.commit()

    def get_user(self, name: str):
        """Получить пользователя по имени"""
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return self.cursor.fetchone()

    def reg_user(self, name: str, password: str):
        """Добавить пользователя в БД"""
        user_token = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO users (name, password, token) VALUES (?, ?, ?)",
            (name, password, user_token)
        )
        self.conn.commit()
        return user_token

    def update_balance(self, name: str, balance: int):
        """Обновить баланс пользователя"""
        self.cursor.execute("UPDATE users SET balance = ? WHERE name = ?", (balance, name))
        self.conn.commit()

    def get_balance(self, name: str):
        """Получить баланс пользователя"""
        self.cursor.execute("SELECT balance FROM users WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def check_user_password(self, name: str, password: str):
        """Аутентификация пользователя"""
        self.cursor.execute("SELECT password FROM users WHERE name = ?", (name,))
        result = self.cursor.fetchone()
        return result[0] == password if result else False
        
    def set_user_token(self, name: str, token: str):
    	"""Устоновить токен для пользователя"""
    	self.cursor.execute("UPDATE users SET token = ? WHERE name = ?", (token, name))
    	self.conn.commit()

    def get_user_by_tg_id(self, tg_user_id: int):
        """Получить пользователя по Telegram ID"""
        self.cursor.execute("SELECT * FROM users WHERE tg_user_id = ?", (tg_user_id,))
        return self.cursor.fetchone()

    def set_tg_user_id(self, name: str, tg_user_id: int):
        """Установить Telegram ID для пользователя"""
        self.cursor.execute("UPDATE users SET tg_user_id = ? WHERE name = ?", (tg_user_id, name))
        self.conn.commit()

    def close(self):
        """Закрыть соединение с БД"""
        self.conn.close()