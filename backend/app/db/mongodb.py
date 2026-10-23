"""
Backward compatibility layer redirecting database requests to Firebase Cloud Firestore.
"""
from app.db.firebase import db_manager, get_db, DatabaseManager

__all__ = ["db_manager", "get_db", "DatabaseManager"]
