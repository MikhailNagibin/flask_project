import flask
from flask import jsonify, make_response, request
from . import db_session
from .books import Books
from .users import User


blueprint = flask.Blueprint(
    "books_api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/books")
def get_books():
    db_sess = db_session.create_session()
    news = db_sess.query(Books).all()
    return jsonify(
        {"books":
             [item.to_dict()
              for item in news]
         }
    )


@blueprint.route("/api/book/<int:id>")
def get_book(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Books).all()
    return jsonify(
        {"book":
             [item.to_dict()
              for item in news if item.id == id]
         }
    )


@blueprint.route('/api/del_book/<int:id>', methods=['DELETE'])
def delete_news(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Books).filter(Books.id == id).first()
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route("/api/jobs/put", methods=["PUT"])
def create_news():
    if not request.json:
        return make_response(jsonify({"error": "Empty request"}), 400)
    elif not all(
        key in request.json for key in ["title", "author", "time_for_reading", "about", "email"]
    ):
        return make_response(jsonify({"error": "Bad request"}), 400)
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.email == request.json["email"]).first()
    if not users:
        return make_response(jsonify({"error": "Bad request"}), 400)
    book = db_sess.query(Books).filter(users.id == Books.whose,
                                       Books.title == request.json["title"]).first()
    if not book:
        return make_response(jsonify({"error": "Bad request"}), 400)
    book.author = request.json['author']
    book.time_for_reading = request.json["time_for_reading"]
    book.about = request.json["about"]
    db_sess.commit()
    return jsonify({"ok": book.id})
