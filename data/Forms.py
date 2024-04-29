from wtforms import *
from flask_wtf import *
from flask_wtf.file import *


class LoginForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    name = StringField("Имя пользователя", validators=[DataRequired()])
    surname = StringField("Фамилия пользователя", validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField("Войти")


class AddBook(FlaskForm):
    title = StringField("Название книги", validators=[DataRequired()])
    author = StringField("Автор", validators=[DataRequired()])
    time_for_reading = IntegerField("время чтения книги", validators=[DataRequired()])
    about = TextAreaField("О книге", validators=[DataRequired()])
    book = FileField("Image File", [validators.regexp(r"^[^/\\]\.jpg$")])
    submit = SubmitField("Добавить")


class Profile(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    name = StringField("Имя пользователя", validators=[DataRequired()])
    surname = StringField("Фамилия пользователя", validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField("Изменить")


class ChangePassword(FlaskForm):
    old_password = PasswordField("Cтарый пароль", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField("Добавить")
