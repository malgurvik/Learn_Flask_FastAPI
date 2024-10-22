"""
Задание №7.
Создать страницу, на которой будет форма для ввода числа
и кнопка "Отправить"
При нажатии на кнопку будет произведено
перенаправление на страницу с результатом, где будет
выведено введенное число и его квадрат.
"""
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        number = request.form.get('number')
        return redirect(url_for('result', number=number))

    return render_template('enter_number.html')


@app.route('/result')
def result():
    number = request.args.get('number')
    res = int(number) ** 2
    return render_template('square_of_the_number.html', number=number, res=res)


@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
