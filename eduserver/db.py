from os import path
from contextlib import contextmanager
from collections import namedtuple, defaultdict

from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.types import DateTime
from sqlalchemy.types import Float

from eduserver.environment import _package_dir

engine = create_engine("sqlite:///{}".format(path.join(_package_dir, 'edu.db')), encoding='utf-8')
Session = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def closing_session():
    session = Session()
    try:
        yield session
    finally:
        session.expunge_all()
        session.commit()
        session.close()

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    user_login = Column(String(128), ForeignKey('users.login'))
    user = relationship("User", foreign_keys=[user_login])
    result = Column(Float)
    date = Column(DateTime)

    def __init__(self, user_login, result, date):
        self.user_login = user_login
        self.result = result
        self.date = date


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    text = Column(String(128))
    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship("Language")

    def __init__(self, text, language):
        self.text = text
        self.language = language


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))

    def __init__(self, title):
        self.title = title


class Translation(Base):
    __tablename__ = 'translations'

    id = Column(Integer, primary_key=True)
    src_word_id = Column(Integer, ForeignKey('words.id'))
    src_word = relationship("Word", foreign_keys=[src_word_id])
    tgt_word_id = Column(Integer, ForeignKey('words.id'))
    tgt_word = relationship("Word", foreign_keys=[tgt_word_id])
    __table_args__ = (UniqueConstraint('src_word_id', 'tgt_word_id', name='uc'),)

    def __init__(self, src_word, tgt_word):
        if src_word.language == tgt_word.language:
            raise RuntimeError('Incorrect translate')
        self.src_word = src_word
        self.tgt_word = tgt_word


class User(Base):
    __tablename__ = 'users'

    IdHolder = namedtuple('IdHolder', ['id'])

    users_translations_association = Table('users_translations', Base.metadata,
                                           Column('user_login', String(128), ForeignKey('users.login')),
                                           Column('translation_id', Integer, ForeignKey('translations.id'))
                                           )

    # id = Column(Integer, primary_key=True)

    login = Column(String(128), primary_key=True)
    password = Column(String(128))
    firstName = Column(String(128))
    lastName = Column(String(128))
    email = Column(String(128))
    dictionary = relationship("Translation", secondary=users_translations_association)
    results = relationship("Result")

    def __init__(self, login, password, first_name, last_name, email):
        self.login = login
        self.password = password
        self.firstName = first_name
        self.lastName = last_name
        self.email = email

    @property
    def id_holder(self):
        return self.IdHolder(self.login)

    @property
    def info(self):
        return {
            'login': self.login,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
        }

    @property
    def translations(self):
        res = defaultdict(list)
        session = Session()

        def get_word(id):
            return session.query(Word).get(id).text

        for k, v in ((get_word(t.src_word_id), get_word(t.tgt_word_id)) for t in self.dictionary):
            res[k].append(v)

        return dict(res)

def initialize_db():
    Base.metadata.create_all(engine)
    with closing_session() as session:
        russian = Language("Russian")
        english = Language("English")
        session.add(russian)
        session.add(english)
