from fastapi import APIRouter

from kb_2315.backend.crud import crud_shoe
from kb_2315.backend.models import Shoe
from kb_2315.backend.schemas import shoe


router = APIRouter()


@router.get("/")
def search_shoe(id: int | None = None, name: str | None = None) -> list[shoe]:
    shoes: list[Shoe] = crud_shoe.search_shoe_by(id=id, name=name)

    return [shoe(id=s.id, name=s.name) for s in shoes]
