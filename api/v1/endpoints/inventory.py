from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from api.deps import get_current_user
from schemas.inventory import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse
from services.inventory import (
    get_inventory_items, get_inventory_item_by_id,
    create_inventory_item, update_inventory_item,
    delete_inventory_item, count_inventory_items
)
from models.base import User

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=List[InventoryItemResponse])
def list_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items = get_inventory_items(db, str(current_user.id), skip, limit)
    return [
        InventoryItemResponse(
            id=str(item.id),
            sku=item.sku,
            name=item.name,
            description=item.description,
            quantity=item.quantity,
            location=item.location,
            rfid_tag=item.rfid_tag,
            user_id=str(item.user_id),
            created_at=item.created_at.isoformat(),
            updated_at=item.updated_at.isoformat()
        )
        for item in items
    ]


@router.post("/", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_data: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = create_inventory_item(db, item_data, str(current_user.id))
    return InventoryItemResponse(
        id=str(item.id),
        sku=item.sku,
        name=item.name,
        description=item.description,
        quantity=item.quantity,
        location=item.location,
        rfid_tag=item.rfid_tag,
        user_id=str(item.user_id),
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat()
    )


@router.get("/{item_id}", response_model=InventoryItemResponse)
def get_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = get_inventory_item_by_id(db, item_id, str(current_user.id))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return InventoryItemResponse(
        id=str(item.id),
        sku=item.sku,
        name=item.name,
        description=item.description,
        quantity=item.quantity,
        location=item.location,
        rfid_tag=item.rfid_tag,
        user_id=str(item.user_id),
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat()
    )


@router.put("/{item_id}", response_model=InventoryItemResponse)
def update_item(
    item_id: str,
    item_data: InventoryItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = update_inventory_item(db, item_id, str(current_user.id), item_data)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return InventoryItemResponse(
        id=str(item.id),
        sku=item.sku,
        name=item.name,
        description=item.description,
        quantity=item.quantity,
        location=item.location,
        rfid_tag=item.rfid_tag,
        user_id=str(item.user_id),
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat()
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_inventory_item(db, item_id, str(current_user.id))
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None