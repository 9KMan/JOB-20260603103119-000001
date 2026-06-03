from pydantic import BaseModel
from typing import Optional


class InventoryItemCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    quantity: int = 0
    location: Optional[str] = None
    rfid_tag: Optional[str] = None


class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    location: Optional[str] = None
    rfid_tag: Optional[str] = None


class InventoryItemResponse(BaseModel):
    id: str
    sku: str
    name: str
    description: Optional[str]
    quantity: int
    location: Optional[str]
    rfid_tag: Optional[str]
    user_id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True