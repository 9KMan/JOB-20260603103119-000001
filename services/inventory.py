from typing import Optional
from sqlalchemy.orm import Session
from models.base import InventoryItem
from schemas.inventory import InventoryItemCreate, InventoryItemUpdate
import uuid


def get_inventory_items(db: Session, user_id: str, skip: int = 0, limit: int = 20) -> list[InventoryItem]:
    return db.query(InventoryItem).filter(
        InventoryItem.user_id == user_id,
        InventoryItem.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_inventory_item_by_id(db: Session, item_id: str, user_id: str) -> Optional[InventoryItem]:
    return db.query(InventoryItem).filter(
        InventoryItem.id == item_id,
        InventoryItem.user_id == user_id,
        InventoryItem.deleted_at.is_(None)
    ).first()


def create_inventory_item(db: Session, item_data: InventoryItemCreate, user_id: str) -> InventoryItem:
    db_item = InventoryItem(
        sku=item_data.sku,
        name=item_data.name,
        description=item_data.description,
        quantity=item_data.quantity,
        location=item_data.location,
        rfid_tag=item_data.rfid_tag,
        user_id=user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_inventory_item(db: Session, item_id: str, user_id: str, item_data: InventoryItemUpdate) -> Optional[InventoryItem]:
    db_item = get_inventory_item_by_id(db, item_id, user_id)
    if not db_item:
        return None
    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_inventory_item(db: Session, item_id: str, user_id: str) -> bool:
    db_item = get_inventory_item_by_id(db, item_id, user_id)
    if not db_item:
        return False
    from datetime import datetime
    db_item.deleted_at = datetime.utcnow()
    db.commit()
    return True


def count_inventory_items(db: Session, user_id: str) -> int:
    return db.query(InventoryItem).filter(
        InventoryItem.user_id == user_id,
        InventoryItem.deleted_at.is_(None)
    ).count()