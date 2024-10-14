"""
Задание №2.
Дорабатываем задачу 1.
Добавьте две дополнительные страницы в ваше веб-приложение:
    ○ страницу "about"
    ○ страницу "contact".
"""
from flask import Flask

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'


@app.route('/about')
def about():
    return 'Страница обо мне'


@app.route('/contact')
def contact():
    return 'Страница с контактами'


if __name__ == '__main__':
    app.run(debug=True)
