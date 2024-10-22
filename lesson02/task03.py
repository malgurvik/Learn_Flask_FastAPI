"""
Задание №3
Создать страницу, на которой будет форма для ввода логина
и пароля
При нажатии на кнопку "Отправить" будет произведена
проверка соответствия логина и пароля и переход на
страницу приветствия пользователя или страницу с
ошибкой.
"""

from flask import Flask, render_template, request
from flask_wtf import FlaskForm

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        if name == 'malgurvik' and password== '1234':
            return 'Welcome!'
        else:
            return 'Nope!'
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)