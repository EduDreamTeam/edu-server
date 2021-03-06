import json
import random

from os import path

import datetime
from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity

from eduserver.db import closing_session, initialize_db, User, Language, Word, Translation, Result
from eduserver.controller import Controller
from eduserver.filter import Filter
import dateutil.parser
from datetime import timedelta

from eduserver.environment import _package_dir


def authenticate(login, password):
    with closing_session() as session:
        user = session.query(User).get(login)
        if user and user.password == password:
            return user.id_holder
        else:
            return None


def identity(payload):
    return payload['identity']


app = Flask(__name__)
app.config.from_pyfile(path.join(_package_dir, 'environment.py'))
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)

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
    with closing_session() as session:
        user = session.query(User).get(str(current_identity))
        return json.dumps(user.info)

@app.route('/dict', methods=('PUT', 'POST'))
@jwt_required()
def process_dict_request_write():
    data = json.loads(request.data.decode())
    str_word = data['word']  # 'dog'
    str_translate = data['translate']  # ['собака', 'пёсик']

    rewrite = {'PUT': False, 'POST': True}[request.method]

    with closing_session() as session:
        user = session.query(User).get(str(current_identity))
        # TODO: realize rewriting
        # TODO: optimize have in translation checking
        if str_word in user.translations:
            return json.dumps(False)

        english = session.query(Language).filter(Language.title == 'English').first()
        russian = session.query(Language).filter(Language.title == 'Russian').first()

        word_en = Word(str_word, english)
        for w in (Word(t, russian) for t in str_translate):
            translation = Translation(word_en, w)
            user.dictionary.append(translation)

    return json.dumps(True)

@app.route('/statistics', methods=('POST', ))
@jwt_required()
def set_statistics():
    with closing_session() as session:
        data = json.loads(request.data.decode())
        result = data['result']
        res = Result(User.login, result, datetime.now())
        user = session.query(User).get(str(current_identity))
        user.results.apend(res)
        return json.dumps(True)

@app.route('/statistics', methods=('GET', ))
@jwt_required()
def get_statistics():
    start = dateutil.parser.parse(request.args.get('startDate'))
    start = start.replace(tzinfo=None)
    end = dateutil.parser.parse(request.args.get('endDate'))
    end = end.replace(tzinfo=None)
    min = float(request.args.get('minResult'))
    max = float(request.args.get('maxResult'))
    controller = Controller()
    filter = Filter(start, end, min, max)
    results = controller.get_results_by_filter(filter)
    # res1 = results[0]
    # res =  {
    #     'date': '2018-12-30T21:00:00.000Z',
    #     'result': 1,
    #     'id': 1
    # }
    res1 = []
    # res1.append(res)
    # res1.append({
    #     'date': '2018-12-31T21:00:00.000Z',
    #     'result': 0.5,
    #     'id': 2
    # })
    for result in results:
        res1.append({
            'date': result.date.isoformat(),
            'result': result.result,
            'id': result.id
        })
    # print("return "+ json.dumps(res))
    return json.dumps(res1)

@app.route('/dict', methods=('GET', ))
@jwt_required()
def process_dict_request_read():
    with closing_session() as session:
        user_dict = session.query(User).get(str(current_identity)).translations
        if request.data:
            data = json.loads(request.data.decode())
            word = data['word']
            if word in user_dict: return json.dumps(user_dict[word])
            else: return json.dumps(False)
            # return json.dumps(['собака', 'пёсик'])
        else:
            return json.dumps(user_dict)
            # return json.dumps({'dog': ['собака', 'пёсик']})


@app.route('/task')
@jwt_required()
def generate_task():
    with closing_session() as session:
        user_dict = session.query(User).get(str(current_identity)).translations

    answers_count = 4

    def generate_one_task(input_dict):
        dict_copy = dict(input_dict)
        word = random.choice(tuple(dict_copy.keys()))
        true_answer = random.choice(dict_copy[word])
        del dict_copy[word]

        answers = []
        for i in dict_copy.values():
            answers.extend(i)
        random.shuffle(answers)

        answers = answers[0: answers_count - 1]
        true_answer_index = random.randrange(0, answers_count - 1)
        answers.insert(true_answer_index, true_answer)

        return {
            'word': word,
            'answers': answers,
            'trueAnswer': true_answer_index,
        }

    return json.dumps([
        generate_one_task(user_dict) for _ in range(5)
    ])


if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0', port=5000)
