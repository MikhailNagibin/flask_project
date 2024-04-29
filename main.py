from flask import *
from flask_login import *
from data.users import User
from data import db_session
from data.Forms import *
from data.books import Books
import datetime
import os
from data import books_api
from data import users_api


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def read():
    db_sess = db_session.create_session()
    books = db_sess.query(Books).all()
    return render_template("read.html", books=books)


@app.route("/register", methods=["GET", "POST"])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            about=form.about.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Авторизация", form=form, message="")


@app.route("/profile")
def profile():
    form = Profile()
    return render_template("profile.html", form=form)


@app.route("/books/read/<int:id>")
def new_read(id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.id == id).first()
    return send_file(book.book)


@app.route("/books/del/<int:id>")
def delate(id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.id == id).first()
    db_sess.delete(book)
    db_sess.commit()
    return redirect("/")


@app.route("/upload", methods=["GET", "POST"])
def add_book():
    form = AddBook()
    if request.method == "POST":
        if "file" not in request.files:
            return render_template(
                "test.html", my_form=form, message="Файл не был загружен."
            )

        file = request.files["file"]
        if file.filename == "":
            return render_template(
                "test.html", my_form=form, message="Файл не был выбран."
            )

        if file:
            filename = os.path.join("templates/books", file.filename)
            file.save(filename)
            db_sess = db_session.create_session()
            book = Books(
                title=form.title.data,
                author=form.author.data,
                time_for_reading=form.time_for_reading.data,
                about=form.about.data,
                whose=current_user.id,
                book=filename,
            )
            db_sess.add(book)
            db_sess.commit()
            return redirect("/")
    return render_template("test.html", my_form=form, message="")


@app.route("/books/<int:id>", methods=["GET", "POST"])
def get_info(id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.id == id).first()
    form = AddBook()
    return render_template("read_about.html", form=form, book=book, block=True)


@app.route("/books/red/<int:id>", methods=["GET", "POST"])
def red(id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.id == id).first()
    form = AddBook()
    if request.method == "POST":
        book.title = form.title.data
        book.author = form.author.data
        book.time_for_reading = form.time_for_reading.data
        book.about = form.about.data
        db_sess.commit()
    return render_template("red.html", form=form, book=book)


@app.route("/redprof", methods=["GET", "POST"])
def redprof():
    form = Profile()
    if request.method == "POST":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.about = form.about.data
        db_sess.commit()
        return redirect("/profile")
    return render_template("profile1.html", form=form)


@app.route("/change_password", methods=["GET", "POST"])
def change():
    form = ChangePassword()
    if request.method == "POST":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        print(form.password.data, form.old_password.data)
        if not user.check_password(form.old_password.data):
            return render_template(
                "change_password.html",
                form=form,
                message="Вы ввели неправильный пароль",
            )
        if form.password.data != form.password_again.data:
            return render_template(
                "change_password.html", form=form, message="Пароли не совпадают"
            )
        if form.password.data == form.old_password.data:
            return render_template(
                "change_password.html",
                form=form,
                message="Вы ввели свой старый пароль",
            )
        user.set_password(form.password.data)
        db_sess.commit()
        return redirect("/profile")
    return render_template("change_password.html", form=form, message="")


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({"error": "Bad Request"}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": error}), 404)


if __name__ == "__main__":
    db_session.global_init("db/books.db")
    app.register_blueprint(books_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8000, host="127.0.0.1")

