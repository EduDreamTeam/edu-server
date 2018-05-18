from eduserver.db import closing_session, initialize_db, User, Language, Word, Translation

from flask_jwt import JWT, jwt_required, current_identity


class DBController:
    def get_results_by_user(self):
        with closing_session() as session:
            results = session.query(User).get(str(current_identity)).results
            return results
