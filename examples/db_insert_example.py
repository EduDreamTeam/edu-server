from eduserver.db import Session, engine, Base
from eduserver.db import Language
from eduserver.db import User
from eduserver.db import Translation
from eduserver.db import Word


def main():
    print('Start')
    Base.metadata.create_all(engine)
    print('Base created')

    session = Session()

    russian = Language("Русский")
    english = Language("English")
    session.add(russian)
    session.add(english)

    word1 = Word("слово1", russian)
    word2 = Word("word2", english)
    session.add(word1)
    session.add(word2)

    translation = Translation(word1, word2)
    session.add(translation)

    if not session.query(User).get('test_user'):
        user = User('test_user', '1234', 'test_first_name', 'test_last_name', 'mail@example.com')
        user.dictionary.append(translation)
        session.add(user)

        session.commit()
        session.close()
        print('User added')

    print('Session closed')


if __name__ == '__main__':
    main()
