from pydantic import BaseModel
from typing import Optional


class OperationCreate(BaseModel):
    type: str
    item_id: str
    quantity_change: int
    notes: Optional[str] = None


class OperationResponse(BaseModel):
    id: str
    type: str
    item_id: str
    quantity_change: int
    notes: Optional[str]
    performed_by: str
    created_at: str

    class Config:
        from_attributes = True