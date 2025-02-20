from pydantic import BaseModel
from typing import Optional

# Pydantic schema for Item (for request/response)
class ItemSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2 (or from_orm=True for v1)
