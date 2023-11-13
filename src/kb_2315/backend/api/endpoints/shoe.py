from fastapi import APIRouter

from kb_2315.backend.crud import crud_shoe
from kb_2315.backend.models import Shoe
from kb_2315.backend.schemas import schema_shoe


router = APIRouter()


@router.get("/")
def search_shoe(id: int | None = None, name: str | None = None) -> list[schema_shoe.shoe]:
    shoes: list[Shoe] = crud_shoe.search_shoe_by(shoe_id=id, name=name)

    return [schema_shoe.shoe(id=s.id, name=s.name) for s in shoes]
