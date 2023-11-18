from uuid import UUID

from sqlalchemy.orm import Query

from kb_2315.backend.models import Session, User
from kb_2315.backend.weather import api as weather_api

from .base_crud import base_CRUD


class CRUD_Session(base_CRUD):
    def add_session(self, user: User, device_id: int, shoe_id: int | None = None) -> UUID:
        with self._Session() as session:
            new_session = Session()
            new_session.shoe_id = shoe_id
            new_session.device_id = device_id
            new_session.weather_code = weather_api.get_weather_code(user.ido_longitude, user.keido_latitude)

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

    def map_session_to_shoe(self, session_id: UUID, shoe_id: int) -> bool:
        with self._Session() as session:
            q: Session | None = session.query(Session).filter(Session.session_id == session_id).first()
            if q and q.shoe_id is None:
                q.shoe_id = shoe_id
                session.commit()
                return True
            else:
                return False


crud_session = CRUD_Session()
