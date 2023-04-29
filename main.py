import os.path
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, redirect, render_template
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'baboo_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', login='путник', title='Home')


@app.route('/cre_site')
def cre_site():
    return render_template('cre_site.html', title='Конструкторы сайтов')


@app.route('/cms')
def CMS():
    return render_template('CMS.html', title='CMS-системы')


@app.route('/html')
def HTML5():
    return render_template('HTML5.html', title='Самостоятельное создание сайта')


@app.route('/java')
def JAVA():
    return render_template('JAVA.html', title='Java')


@app.route('/php')
def PHP():
    return render_template('PHP.html', title='PHP')


@app.route('/python')
def PYTHON():
    return render_template('PYTHON.html', title='PYTHON')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/home")


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=2007, host='127.0.0.1', debug=True)
