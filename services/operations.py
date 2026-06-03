from sqlalchemy.orm import Session
from models.base import Operation, OperationType, InventoryItem
from schemas.operations import OperationCreate
from datetime import datetime


def get_operations(db: Session, user_id: str, skip: int = 0, limit: int = 20) -> list[Operation]:
    return db.query(Operation).join(InventoryItem).filter(
        InventoryItem.user_id == user_id
    ).order_by(Operation.created_at.desc()).offset(skip).limit(limit).all()


def create_operation(db: Session, op_data: OperationCreate, user_id: str) -> Operation:
    db_op = Operation(
        type=OperationType(op_data.type),
        item_id=op_data.item_id,
        quantity_change=op_data.quantity_change,
        notes=op_data.notes,
        performed_by=user_id
    )
    db.add(db_op)
    db.commit()
    db.refresh(db_op)
    return db_op