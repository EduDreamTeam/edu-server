from sqlalchemy import *
from sqlalchemy.orm import *
from eduserver.db.entity.base import Base
from eduserver.db.entity.language import Language


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    text = Column(String(128))
    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship("Language")

    def __init__(self, text, language):
        self.text = text
        self.language = language
