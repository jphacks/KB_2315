from pydantic import BaseModel


class shoe(BaseModel):
    id: int
    name: str
