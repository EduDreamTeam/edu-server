from os import path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from eduserver.environment import _package_dir

engine = create_engine("sqlite:///{}".format(path.join(_package_dir, 'edu.db')), encoding='utf-8')
Session = sessionmaker(bind=engine)

Base = declarative_base()
