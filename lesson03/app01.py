"""
Задание №1
Создать базу данных для хранения информации о студентах университета.
База данных должна содержать две таблицы: "Студенты" и "Факультеты".
В таблице "Студенты" должны быть следующие поля: id, имя, фамилия,
возраст, пол, группа и id факультета.
В таблице "Факультеты" должны быть следующие поля: id и название
факультета.
Необходимо создать связь между таблицами "Студенты" и "Факультеты".
Написать функцию-обработчик, которая будет выводить список всех
студентов с указанием их факультета.
"""
from random import randint, choice

from flask import Flask, render_template, redirect, url_for
from lesson03.model01 import db, Student, Faculty

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Initialized database.')


@app.cli.command('fill-tbl')
def fill_tbl():
    for i in range(1, 6):
        faculty = Faculty(
            name=f'Faculty{i}'
        )
        db.session.add(faculty)
        db.session.commit()

    for i in range(1, 11):
        student = Student(
            first_name=f'FirstName{i}',
            last_name=f'LastName{i}',
            age=randint(18, 60),
            gender=choice([True, False]),
            group=randint(1, 6),
            faculty_id=randint(1, 5)
        )
        db.session.add(student)
        db.session.commit()


@app.route('/')
def index():
    students = Student.query.all()
    print(students)
    return render_template('students.html', students=students)


@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
