from fastapi import APIRouter
from app.db.firebase import db_manager, get_db
from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    if not db_manager.is_connected:
        get_db()
    
    db_status = "connected" if db_manager.is_connected else "disconnected"
    database_type = "firestore_mock" if db_manager.is_mock else "firebase_firestore"

    return {
        "status": "healthy",
        "service": "RuralConnect Karnataka API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "database": {
            "status": db_status,
            "type": database_type,
            "project_id": settings.FIREBASE_PROJECT_ID,
        },
    }
