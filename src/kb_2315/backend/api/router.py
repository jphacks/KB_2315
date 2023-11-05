from fastapi import APIRouter

from .endpoints import line, sensor, session, shoe


api_router = APIRouter()

api_router.include_router(sensor.router, prefix="/sensor", tags=["hook"])
api_router.include_router(shoe.router, prefix="/shoe", tags=["hook"])
api_router.include_router(session.router, prefix="/session", tags=["hook"])
api_router.include_router(line.router, prefix="/", tags=["hook"])
