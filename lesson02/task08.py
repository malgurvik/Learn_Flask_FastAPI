"""
Задание №8.
Создать страницу, на которой будет форма для ввода имени
и кнопка "Отправить"
При нажатии на кнопку будет произведено
перенаправление на страницу с flash сообщением, где будет
выведено "Привет, {имя}!".
"""

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = b'9a4ea9bad8a9d31c80b96b71758cf45d2210a896081c87a8b74720df5d8570f8'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Введите имя!')
            return redirect(url_for('index'))
        flash(f'Привет, {request.form['name']}!')
        return redirect(url_for('index'))
    return render_template('hi.html')


@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
