from sqlalchemy import *
from sqlalchemy.orm import *
from eduserver.db.entity.base import Base
from eduserver.db.entity.word import Word

class Translation(Base):
    __tablename__ = 'translations'

    id = Column(Integer, primary_key=True)
    src_word_id = Column(Integer, ForeignKey('words.id'))
    src_word = relationship("Word", foreign_keys=[src_word_id])
    tgt_word_id = Column(Integer, ForeignKey('words.id'))
    tgt_word = relationship("Word", foreign_keys=[tgt_word_id])
    __table_args__ = (UniqueConstraint('src_word_id', 'tgt_word_id', name='uc'), )

    def __init__(self, src_word, tgt_word):
        self.src_word = src_word
        self.tgt_word = tgt_word
