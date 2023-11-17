from uuid import uuid4

from sqlalchemy.orm import Query

from kb_2315.backend.models import User

from .base_crud import base_CRUD


class CRUD_User(base_CRUD):
    def add_user(self, name: str = f"User-{str(uuid4())[:8]}") -> int:
        new_user = User()
        new_user.name = name

        with self._Session() as session:
            session.add(new_user)
            session.commit()

        return new_user.id

    def search_user_by(
        self,
        user_id: int | None = None,
        name: str | None = None,
    ) -> list[User]:
        with self._Session() as session:
            query: Query[User] = session.query(User)

            if name is not None:
                query = query.filter(User.name.like(f"%{name}%"))
            if user_id is not None:
                query = query.filter(User.id == user_id)

            return query.all()

    def set_line_channel_id_by_user_id(self, user_id: int, line_channel_id: str) -> None:
        with self._Session() as session:
            u: User | None = session.query(User).filter(User.id == user_id).first()

            if u is not None:
                u.line_channel_id = line_channel_id
            session.commit()


crud_user = CRUD_User()
