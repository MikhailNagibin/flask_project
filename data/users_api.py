import flask
from flask import jsonify, make_response, request
from . import db_session
from .users import User


blueprint = flask.Blueprint(
    "users_api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/Users/<int:id>")
def get_new(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    if user:
        return jsonify(
            {"news":
                 [user.to_dict()]
             }
        )
    return jsonify({"error": "Not found"})


@blueprint.route("/api/Users")
def get_news():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    if user:
        return jsonify(
            {"users":
                 [item.to_dict()
                  for item in user]
             }
        )
    return jsonify({"error": "Not found"})


@blueprint.route('/api/del_user/<int:id>', methods=['DELETE'])
def delete_news(id):
    db_sess = db_session.create_session()
    news = db_sess.query(User).filter(User.id == id).first()
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route("/api/new_user", methods=["POST"])
def new():
    if not request.json:
        return make_response(jsonify({"error": "Empty request"}), 400)
    elif not all(
        key in request.json for key in ["name", "surname", "about", "email", "hashed_password"]
    ):
        return make_response(jsonify({"error": "Bad request"}), 400)
    db_sess = db_session.create_session()
    user = User(
            name=request.json["name"],
            surname=request.json["surname"],
            email=request.json["email"],
            about=request.json["about"],
        )
    user.set_password(request.json["hashed_password"])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': user.id})


@blueprint.route("/api/user/change_password", methods=["PUT"])
def change():
    if not request.json:
        return make_response(jsonify({"error": "Empty request"}), 400)
    elif not all(
        key in request.json for key in ["old_password", "new_password", "email"]
    ):
        return make_response(jsonify({"error": "Bad request"}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == request.json['email']).first()
    if not user:
        return make_response(jsonify({"error": "Bad request"}), 400)
    if not user.check_password(request.json["old_password"]):
        return make_response(jsonify({"error": "Bad request"}), 400)
    user.set_password(request.json["new_password"])
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route("/api/user/change_info", methods=["PUT"])
def change2():
    if not request.json:
        return make_response(jsonify({"error": "Empty request"}), 400)
    elif not all(
        key in request.json for key in ["name", "surname", "about", "email"]
    ):
        return make_response(jsonify({"error": "Bad request"}), 400)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == request.json['email']).first()
    user.name = request.json["name"]
    user.surname = request.json["surname"]
    user.about = request.json['about']
    db_sess.commit()
    return jsonify({'success': user.id})
