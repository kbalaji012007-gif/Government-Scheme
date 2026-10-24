from fastapi import APIRouter
from app.db.mongodb import db_manager
from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    db_status = "disconnected"
    database_type = "unknown"
    if db_manager.is_connected:
        db_status = "connected"
        database_type = "mongomock" if db_manager.is_mock else "mongodb"

    return {
        "status": "healthy",
        "service": "RuralConnect Karnataka API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "database": {
            "status": db_status,
            "type": database_type,
            "database_name": settings.DATABASE_NAME,
        },
    }
