from fastapi import APIRouter
from api.v1.endpoints import auth, inventory, operations

router = APIRouter()
router.include_router(auth.router)
router.include_router(inventory.router)
router.include_router(operations.router)