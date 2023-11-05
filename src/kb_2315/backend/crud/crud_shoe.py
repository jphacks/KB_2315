from uuid import uuid4

from sqlalchemy.orm import Query

from kb_2315.backend.models import Shoe

from .base_crud import base_CRUD


class CRUD_Shoe(base_CRUD):
    def add_shoe(self, name: str = f"Shoe-{str(uuid4())[:8]}") -> None:
        new_shoe = Shoe()
        new_shoe.name = name

        with self._Session() as session:
            session.add(new_shoe)
            session.commit()

    def search_shoe_by(
        self,
        id: int | None = None,
        name: str | None = None,
    ) -> list[Shoe]:
        with self._Session() as session:
            query: Query[Shoe] = session.query(Shoe)

            if name is not None:
                query = query.filter(Shoe.name == name)
            if id is not None:
                query = query.filter(Shoe.id == id)

            return query.all()


crud_shoe = CRUD_Shoe()
