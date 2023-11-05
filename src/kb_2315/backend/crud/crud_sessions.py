from uuid import UUID

from sqlalchemy.orm import Query

from kb_2315.backend.models import Sessions

from .base_crud import base_CRUD


class CRUD_Sessions(base_CRUD):
    def add_session(self, shoe_id: int | None = None) -> None:
        with self._Session() as session:
            new_session = Sessions()
            new_session.shoe_id = shoe_id

            session.add(new_session)
            session.commit()

    def search_session_by(
        self,
        id: int | None = None,
        shoe_id: int | None = None,
        session_id: UUID | None = None,
    ) -> list[Sessions]:
        with self._Session() as session:
            query: Query[Sessions] = session.query(Sessions)

            if id is not None:
                query = query.filter(Sessions.id == id)
            if shoe_id is not None:
                query = query.filter(Sessions.shoe_id == shoe_id)
            if session_id is not None:
                query = query.filter(Sessions.session_id == session_id)

            return query.all()

    def map_session_to_shoe(self, session_id: UUID, shoe_id: int) -> None:
        with self._Session() as session:
            session.query(Sessions).filter(Sessions.session_id == session_id).update({Sessions.shoe_id: shoe_id})
            session.commit()


crud_sessions = CRUD_Sessions()
