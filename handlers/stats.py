from flask import jsonify

def stats_handlers(app, db):
    @app.route('/top', methods=['GET'])
    def _top_10():
        db.cursor.execute("SELECT name, balance FROM users ORDER BY balance DESC LIMIT 10")
        stats = db.cursor.fetchall()

        if not stats:
            return jsonify({"message": "Пусто"}), 200

        result = [{"rank": i+1, "name": name, "balance": balance} for i, (name, balance) in enumerate(stats)]
        
        # Если меньше 10 записей, добавляем пустые записи
        if len(stats) < 10:
            result += [{"rank": i+1, "name": "Пусто", "balance": 0} for i in range(len(stats), 10)]

        return jsonify(result), 200