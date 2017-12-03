import json
import os

from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from flask_sqlalchemy import SQLAlchemy


class User(object):
    __slots__ = ('id', 'username', 'password')

    def __init__(self, identifier, username, password):
        self.id = identifier
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='{}')".format(self.id)


user = User(1, 'user', 'password')


def authenticate(username, password):
    if username == user.username and password == user.password:
        return user


def identity(payload):
    return payload['identity']


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')

jwt = JWT(app, authenticate, identity)

db = SQLAlchemy(app)

# send CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


@app.route('/register', methods=('POST', ))
def register_new_user():
    data = json.loads(request.data.decode())
    print(data)
    return json.dumps(True)


@app.route('/unprotected')
def unprotected():
    return json.dumps({
        'message': 'This is an unprotected resource.'
    })


@app.route('/protected')
@jwt_required()
def protected():
    return json.dumps({
        'message': 'This is a protected resource.',
        'current_identity': str(current_identity)
    })


if __name__ == '__main__':
    app.run()
