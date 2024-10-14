"""
Задание №6.
Написать функцию, которая будет выводить на экран HTML
страницу с таблицей, содержащей информацию о студентах.
Таблица должна содержать следующие поля: "Имя",
"Фамилия", "Возраст", "Средний балл".
Данные о студентах должны быть переданы в шаблон через
контекст.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/students/')
def students_info():
    students = [
        {'name': 'John', 'last_name': 'Doe', 'age': 25, 'average_score': 85},
        {'name': 'Jane', 'last_name': 'Smith', 'age': 22, 'average_score': 90},
        {'name': 'Bob', 'last_name': 'Johnson', 'age': 23, 'average_score': 78},
    ]
    return render_template('students.html', students=students)


if __name__ == '__main__':
    app.run(debug=True)
