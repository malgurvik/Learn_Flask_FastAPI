"""
Задание №4
Создать страницу, на которой будет форма для ввода текста и
кнопка "Отправить"
При нажатии кнопки будет произведен подсчет количества слов
в тексте и переход на страницу с результатом.
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        words_count = len(text.split())
        return render_template('number_of_words.html', words_count=words_count)
    return render_template('count_word.html')

@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
