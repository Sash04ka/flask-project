import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Получаем URL базы данных из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Подключение к PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Создадим таблицу, если её нет
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
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    return redirect('/users')

@app.route('/users')
def users():
    cursor.execute("SELECT * FROM users")
    users_list = cursor.fetchall()
    return render_template('users.html', users=users_list)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)
