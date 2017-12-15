from eduserver.db.entity.base import Session
from eduserver.db.entity.user import User

session = Session()
class DBController:
    session = Session()

    @staticmethod
    def get_users():
        return session.query(User).all()

    def get_dictionary_by_user(self):
        usr = session.query(User).get(self.id)
        return usr.dictionary
