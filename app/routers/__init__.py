from fastapi import APIRouter
from .tables import router as tables_router
from .reservations import router as reservations_router

api_router = APIRouter()
api_router.include_router(tables_router)
api_router.include_router(reservations_router)
