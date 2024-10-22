"""
Задание №9.
Создать страницу, на которой будет форма для ввода имени
и электронной почты.
При отправке которой будет создан cookie файл с данными
пользователя
Также будет произведено перенаправление на страницу
приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка "Выйти"
При нажатии на кнопку будет удален cookie файл с данными
пользователя и произведено перенаправление на страницу
ввода имени и электронной почты.
"""

from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash

app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        if name and email:
            response = make_response(redirect(url_for('greeting')))
            response.set_cookie('name', name)
            response.set_cookie('email', email)
            return response
        else:
            flash('Please fill all fields.')

    return render_template('log_in.html')


@app.route('/greeting/')
def greeting():
    name = request.cookies.get('name')
    email = request.cookies.get('email')

    if name and email:
        return render_template('greeting.html', name=name)
    else:
        return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('name')
    response.delete_cookie('email')
    return response


@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
