"""
Задание №4.
Написать функцию, которая будет принимать на вход строку и
выводить на экран ее длину.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/string_length/<string:text>')
def sum_nums(text):
    return f'Длинна строки равна: {len(text)}'


if __name__ == '__main__':
    app.run(debug=True)
