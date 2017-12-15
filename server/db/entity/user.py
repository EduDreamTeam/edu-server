from sqlalchemy import *
from sqlalchemy.orm import *
from server.db.entity.base import Base
from server.db.entity.translation import Translation

users_translations_association = Table('users_translations', Base.metadata,
                                     Column('user_id', Integer, ForeignKey('users.id')),
                                     Column('translation_id', Integer, ForeignKey('translations.id'))
                                     )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    password = Column(String(128))
    dictionary = relationship("Translation", secondary=users_translations_association)

    def __init__(self, name, password):
        self.name = name
        self.password = password
