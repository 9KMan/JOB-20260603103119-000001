from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from api.deps import get_current_user
from schemas.operations import OperationCreate, OperationResponse
from services.operations import get_operations, create_operation
from services.inventory import get_inventory_item_by_id
from models.base import User

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.get("/", response_model=List[OperationResponse])
def list_operations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ops = get_operations(db, str(current_user.id), skip, limit)
    return [
        OperationResponse(
            id=str(op.id),
            type=op.type.value,
            item_id=str(op.item_id),
            quantity_change=int(op.quantity_change),
            notes=str(op.notes) if op.notes else None,
            performed_by=str(op.performed_by),
            created_at=op.created_at.isoformat()
        )
        for op in ops
    ]


@router.post("/", response_model=OperationResponse, status_code=201)
def create_new_operation(
    op_data: OperationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = get_inventory_item_by_id(db, op_data.item_id, str(current_user.id))
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    op = create_operation(db, op_data, str(current_user.id))
    return OperationResponse(
        id=str(op.id),
        type=op.type.value,
        item_id=str(op.item_id),
        quantity_change=int(op.quantity_change),
        notes=str(op.notes) if op.notes else None,
        performed_by=str(op.performed_by),
        created_at=op.created_at.isoformat()
    )