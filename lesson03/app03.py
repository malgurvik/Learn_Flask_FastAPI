"""
Задание №4.
Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
содержать следующие поля:
    ○ Имя пользователя (обязательное поле)
    ○ Электронная почта (обязательное поле, с валидацией на корректность ввода email)
    ○ Пароль (обязательное поле, с валидацией на минимальную длину пароля)
    ○ Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
заполнено или данные не прошли валидацию, то должно выводиться соответствующее
сообщение об ошибке.
Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
об ошибке.
"""

from random import randint, choice

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import CSRFProtect

from lesson03.model03 import db, User
from lesson03.form01 import RegistrationForm, LoginForm

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = '84a4cd3864b25221007a74befb9e6f924150af55d6a8a1bca4bd4e2c81a7428a'
csrf = CSRFProtect(app)
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Initialized database.')


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/login/', methods=['GET', 'POST'])
@csrf.exempt
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        print(user)
        if user:
            flash('Logged in successfully.')
            return render_template('welcome.html', username=username)
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists.')
            return redirect(url_for('registration'))
        user = User(
            username=username,
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful.')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
