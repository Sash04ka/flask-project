import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# Проверяем, что DATABASE_URL установлен
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не задан. Убедитесь, что переменная окружения установлена.")

# Функция для получения подключения
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

# Создадим таблицу, если её нет
with get_db_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
    return redirect('/users')

@app.route('/users')
def users():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users_list = cursor.fetchall()
    return render_template('users.html', users=users_list)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)
