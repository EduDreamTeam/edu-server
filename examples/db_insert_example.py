from eduserver.db.entity.base import Session, engine, Base
from eduserver.db.entity.language import Language
from eduserver.db.entity.user import User
from eduserver.db.entity.translation import Translation
from eduserver.db.entity.word import Word

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

    user = User("John", "password")
    user.dictionary.append(translation)

    session.add(user)
    session.commit()
    session.close()

    print('Session closed')

if __name__ == '__main__':
    main()
