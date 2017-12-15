import json

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


app = Flask(__name__)
app.config.from_object('config.BaseConfig')

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
    print('firstName: {}'.format(data['firstName']))
    print('lastName: {}'.format(data['lastName']))
    print('email: {}'.format(data['email']))
    print('login: {}'.format(data['login']))
    print('password: {}'.format(data['password']))
    return json.dumps(data['username'] != 'failed')


@app.route('/userinfo')
@jwt_required()
def get_user_info():
    return json.dumps({
        'firstName': 'Petr',
        'lastName': 'Popadi',
        'email': 'petrpopadi@example.com',
        'login': 'petr_popadi',
    })


@app.route('/dict', methods=('PUT', 'POST'))
@jwt_required()
def process_dict_request_write():
    data = json.loads(request.data.decode())
    word = data['word']  # 'dog'
    translate = data['translate']  # ['собака', 'пёсик']
    if request.method == 'PUT':
        # if word in user_dict: return json.dumps(False)
        # user_dict.write(word, translate)
        return json.dumps(True)
    elif request.method == 'POST':
        # user_dict.write(word, translate)
        return json.dumps(True)
    else:
        raise RuntimeError('Unknown method')


@app.route('/dict', methods=('GET', ))
@jwt_required()
def process_dict_request_read():
    if request.data:
        data = json.loads(request.data.decode())
        word = data['word']
        # if word in user_dict: return json.dumps(user_dict['word'])
        # else: return json.dumps(False)
        return json.dumps(['собака', 'пёсик'])
    else:
        # return json.dumps(user_dict)
        return json.dumps({'dog': ['собака', 'пёсик']})


@app.route('/task')
@jwt_required()
def generate_task():
    return json.dumps([
        {
            'word': 'dog',
            'answers': ['кот', 'машина', 'собака', 'морковь'],
            'trueAnswer': 2,
        },
        {
            'word': 'cat',
            'answers': ['девочка', 'кот', 'ножницы', 'тёща'],
            'trueAnswer': 1,
        },
    ])


if __name__ == '__main__':
    app.run()
