from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://root:root@localhost:3306/edu_db?charset=utf8", encoding='utf-8')
Session = sessionmaker(bind=engine)

Base = declarative_base()
