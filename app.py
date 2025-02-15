from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Подключение к PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")  # Переменная окружения из Render
conn = psycopg2.connect(DATABASE_URL)

cursor = conn.cursor()

# Создадим таблицу пользователей, если ее нет
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()

# Главная страница с формой для добавления пользователей
@app.route('/')
def index():
    return render_template('index.html')

# Добавление пользователя в БД
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    return redirect('/users')

# Список пользователей
@app.route('/users')
def users():
    cursor.execute("SELECT * FROM users")
    users_list = cursor.fetchall()
    return render_template('users.html', users=users_list)

# Удаление пользователя
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)
