import json

from os import path

from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity

from eduserver.db import closing_session, engine, Base, User

from eduserver.environment import _package_dir


def authenticate(login, password):
    print('find User:', login, password)
    with closing_session() as session:
        user = session.query(User).get(login)
        if user and user.password == password:
            print('User find')
            return user.get_id_holder()
        else:
            print('User NOT find')
            return None


def identity(payload):
    return payload['identity']


app = Flask(__name__)
app.config.from_pyfile(path.join(_package_dir, 'environment.py'))

jwt = JWT(app, authenticate, identity)

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
    # TODO: validate data
    user = User(
        login=data['login'],
        password=data['password'],
        first_name=data['firstName'],
        last_name=data['lastName'],
        email=data['email']
    )
    with closing_session() as session:
        if not session.query(User).get(user.login):
            session.add(user)
            return json.dumps(True)
        return json.dumps(False)


@app.route('/userinfo')
@jwt_required()
def get_user_info():
    print(current_identity)
    with closing_session() as session:
        user = session.query(User).get(str(current_identity))
        return json.dumps(user.get_info())


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

# @app.route('/users')
# def get_users():
#     # users = session.query(User)
#     users = DBController.get_users()
#     return json.dumps({
#         'First user: ': users[0].name
#     })
#
# @app.route('/dictionary')
# def get_dictionary_by_user():
#     users = DBController.get_users()
#     dict = DBController.get_dictionary_by_user(users[0])
#     return json.dumps({
#         'First target word in dictionary is ': dict[0].tgt_word.text
#     })

if __name__ == '__main__':
    app.run()
