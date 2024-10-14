"""
Задание №7.
Написать функцию, которая будет выводить на экран HTML
страницу с блоками новостей.
Каждый блок должен содержать заголовок новости,
краткое описание и дату публикации.
Данные о новостях должны быть переданы в шаблон через
контекст.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/news')
def news_page():
    news_data = [
        {'title': 'Новость 1', 'description': 'Описание новости 1', 'date': '2022-01-01'},
        {'title': 'Новость 2', 'description': 'Описание новости 2', 'date': '2022-02-01'}
    ]
    return render_template('news.html', news_data=news_data)


if __name__ == '__main__':
    app.run(debug=True)
