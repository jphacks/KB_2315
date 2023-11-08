from uuid import UUID

from sqlalchemy.orm import Query

from kb_2315.backend.models import Session

from .base_crud import base_CRUD


class CRUD_Session(base_CRUD):
    def add_session(self, device_id: int, shoe_id: int | None = None) -> UUID:
        with self._Session() as session:
            new_session = Session()
            new_session.shoe_id = shoe_id
            new_session.device_id = device_id

            session.add(new_session)
            session.commit()

            sid: UUID = new_session.session_id

        return sid

    def search_session_by(
        self,
        id: int | None = None,
        device_id: int | None = None,
        shoe_id: int | None = None,
        session_id: UUID | None = None,
    ) -> list[Session]:
        with self._Session() as session:
            query: Query[Session] = session.query(Session)

            if id is not None:
                query = query.filter(Session.id == id)
            if device_id is not None:
                query = query.filter(Session.device_id == device_id)
            if shoe_id is not None:
                query = query.filter(Session.shoe_id == shoe_id)
            if session_id is not None:
                query = query.filter(Session.session_id == session_id)

            return query.all()

    def map_session_to_shoe(self, session_id: UUID, shoe_id: int) -> None:
        with self._Session() as session:
            session.query(Session).filter(Session.session_id == session_id).update({Session.shoe_id: shoe_id})
            session.commit()


crud_session = CRUD_Session()
