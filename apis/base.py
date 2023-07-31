from fastapi import APIRouter
from apis import transactions

api_router = APIRouter()

#api_router.include_router(route_general_pages.general_pages_router,prefix="",tags=["general_pages"])
api_router.include_router(transactions.router)