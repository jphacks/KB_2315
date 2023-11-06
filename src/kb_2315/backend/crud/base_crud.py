from sqlalchemy.orm import scoped_session, sessionmaker

from kb_2315.backend.db.session import engine


class base_CRUD:
    def __init__(self) -> None:
        self._Session = scoped_session(sessionmaker(bind=engine))
