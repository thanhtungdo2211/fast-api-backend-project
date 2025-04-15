from fastapi.routing import APIRouter 

from api import auth, monitoring, items

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(monitoring.router, tags=["Healthcheck"])
api_router.include_router(items.router, tags=["Items"])