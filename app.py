from flask import Flask, jsonify, request, session
from flask_restful import Api, Resource
from flaskext.mysql import MySQL
import os
from functools import wraps
import jwt

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("PURE_SECRET_KEY")
app.config["MYSQL_DATABASE_HOST"] = os.environ.get("PURE_DATABASE_HOST")
app.config["MYSQL_DATABASE_USER"] = os.environ.get("PURE_DATABASE_USER")
app.config["MYSQL_DATABASE_PASSWORD"] = os.environ.get(
    "PURE_DATABASE_PASSWORD")
app.config["MYSQL_DATABASE_DB"] = os.environ.get("PURE_DATABASE_DB")
app.config["MYSQL_DATABASE_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
mysql.init_app(app)
api = Api(app)


def private(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({
                "message": "Forbidden",
                "status_code": 403
            })
        else:
            try:
                data = jwt.decode(
                    token, app.config['SECRET_KEY'], algorithms="HS256")
            except Exception:
                return jsonify({
                    "message": "invalid token",
                    "status_code": 403
                })
        return func(*args, **kwargs)
    return wrapped


class Test(Resource):
    def post(self):  # test
        pass


api.add_resource(Test, "/users")


if __name__ == "__main__":
    app.run(debug=True)
