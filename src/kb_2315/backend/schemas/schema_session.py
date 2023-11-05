from pydantic import BaseModel


class create_session(BaseModel):
    shoe_id: int
