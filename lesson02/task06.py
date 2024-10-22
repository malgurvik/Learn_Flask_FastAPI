"""
Задание №6.
Создать страницу, на которой будет форма для ввода имени
и возраста пользователя и кнопка "Отправить"
При нажатии на кнопку будет произведена проверка
возраста и переход на страницу с результатом или на
страницу с ошибкой в случае некорректного возраста.
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        name = request.form.get('name')
        age = request.form.get('age')

        if age.isdigit() and int(age) >= 18:
            return redirect(url_for('result', name=name, age=age))
        else:
            return render_template('error.html', age=age)
    return render_template('name_age.html')


@app.route('/access')
def result():
    name = request.args.get('name')
    age = request.args.get('age')
    return render_template('access_open.html', name=name, age=age)


@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
