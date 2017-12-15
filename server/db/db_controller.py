from db.entity.base import Session
from db.entity.user import User

session = Session()
class DBController:
    session = Session()


    def get_users():
        return session.query(User).all()

    def get_dictionary_by_user(user):
        usr = session.query(User).get(user.id)
        return usr.dictionary;