import json
import os

from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from flask_sqlalchemy import SQLAlchemy

from db.entity.base import Session, engine, Base
from db.entity.user import User
from db.db_controller import DBController



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

@app.route('/users')
def get_users():
    # users = session.query(User)
    users = DBController.get_users()
    return json.dumps({
        'First user: ': users[0].name
    })

@app.route('/dictionary')
def get_dictionary_by_user():
    users = DBController.get_users()
    dict = DBController.get_dictionary_by_user(users[0])
    return json.dumps({
        'First target word in dictionary is ': dict[0].tgt_word.text
    })

if __name__ == '__main__':
    app.run()
