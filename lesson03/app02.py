"""Задание №2
Создать базу данных для хранения информации о книгах в библиотеке.
База данных должна содержать две таблицы: "Книги" и "Авторы".
В таблице "Книги" должны быть следующие поля: id, название, год издания,
количество экземпляров и id автора.
В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
Необходимо создать связь между таблицами "Книги" и "Авторы".
Написать функцию-обработчик, которая будет выводить список всех книг с
указанием их авторов.
"""
from random import randint, choice

from flask import Flask, render_template, redirect, url_for
from lesson03.model02 import db, Author, Books

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Initialized database.')


@app.cli.command('fill-tbl')
def fill_tbl():
    for i in range(1, 6):
        author = Author(
            first_name=f'First_name{i}',
            second_name=f'Second_name{i}'
        )
        db.session.add(author)
        db.session.commit()

    for i in range(1, 11):
        book = Books(
            book_title=f'Title{i}',
            year_of_publication=randint(1970, 2024),
            number_of_copies=randint(1000, 10000),
            author_id=randint(1, 5)
        )
        db.session.add(book)
        db.session.commit()


@app.route('/')
def index():
    books = Books.query.all()
    return render_template('books.html', books=books)


@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)