from server.db.entity.base import Session, engine, Base
from server.db.entity.language import Language
from server.db.entity.user import User
from server.db.entity.translation import Translation
from server.db.entity.word import Word


Base.metadata.create_all(engine)


session = Session()




russian = Language("Русский")
english = Language("English")
session.add(russian)
session.add(english)


word1 = Word("слово1", russian)
word2 = Word("word2", english)
session.add(word1)
session.add(word1)


translation = Translation(word1, word2)
session.add(translation)

user = User("John", "password")
user.dictionary.append(translation)
session.add(user)




session.commit


session.commit()
session.close()
