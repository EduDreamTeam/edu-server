from eduserver.db import Session, engine, Base
from eduserver.db import Language
from eduserver.db import User
from eduserver.db import Translation
from eduserver.db import Word
from eduserver.db import Result
from datetime import datetime


def main():
    print('Start')
    Base.metadata.create_all(engine)
    print('Base created')

    session = Session()

    russian = Language("Russian")
    english = Language("English")
    session.add(russian)
    session.add(english)

    word1 = Word("word2", english)
    word2 = Word("слово1", russian)
    session.add(word1)
    session.add(word2)

    translation = Translation(word1, word2)

    try:
        Translation(word1, word1)
    except RuntimeError as e:
        print(e)

    session.add(translation)

    if not session.query(User).get('test_user'):
        user = User('test_user', '1234', 'test_first_name', 'test_last_name', 'mail@example.com')
        user.dictionary.append(translation)
        result = Result(user, 0.6, datetime.now())
        user.results.append(result)
        session.add(user)

        session.commit()
        session.close()
        print('User added')

    print('Session closed')


if __name__ == '__main__':
    main()
