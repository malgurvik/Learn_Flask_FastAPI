"""
Задание №3.
Написать функцию, которая будет принимать на вход два
числа и выводить на экран их сумму.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/sum_nums/<path:num>')
def sum_nums(num):
    num1, num2 = map(int, num.split('+'))
    return str(num1 + num2)


if __name__ == '__main__':
    app.run(debug=True)
