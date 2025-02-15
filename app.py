from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Подключение к MySQL
conn = mysql.connector.connect(
    user="root",
    host="localhost",
    password="1234",  # Укажи свой пароль
    database="my_new_db"  # Укажи свою базу
)
cursor = conn.cursor()

# ✅ Главная страница (форма для добавления пользователей)
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Добавление пользователя в MySQL
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    return redirect('/users')

# ✅ Вывод всех пользователей
@app.route('/users')
def list_users():
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    return render_template('users.html', users=users)

# ✅ Удаление пользователя
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    return redirect('/users')

if __name__ == "__main__":
    app.run(debug=True)
