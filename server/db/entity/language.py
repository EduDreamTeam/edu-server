from sqlalchemy import *
from sqlalchemy.orm import *
from server.db.entity.base import Base


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))

    def __init__(self, title):
        self.title = title

