from uuid import UUID

from pydantic import BaseModel


class create_session(BaseModel):
    session_id: UUID
