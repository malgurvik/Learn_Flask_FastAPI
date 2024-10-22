"""
Задание №5.
Создать страницу, на которой будет форма для ввода двух
чисел и выбор операции (сложение, вычитание, умножение
или деление) и кнопка "Вычислить"
При нажатии на кнопку будет произведено вычисление
результата выбранной операции и переход на страницу с
результатом.
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num1 = float(request.form.get('num1'))
        num2 = float(request.form.get('num2'))
        operation = request.form.get('operation')
        result = None

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                return 'Error: Division by zero'

        return render_template('calc_result.html', result=result)

    return render_template('calculator.html')


# @app.route('/result')
# def result():
#     return render_template('calc_result.html', result)


@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
