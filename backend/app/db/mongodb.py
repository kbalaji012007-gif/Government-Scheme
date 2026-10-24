import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
import mongomock
from app.core.config import settings

logger = logging.getLogger("ruralconnect.db")


class DatabaseManager:
    client: Optional[MongoClient] = None
    db: Optional[Database] = None
    is_connected: bool = False
    is_mock: bool = False

    def connect(self, uri: Optional[str] = None, force_mock: bool = False) -> None:
        target_uri = uri or settings.MONGODB_URI
        if force_mock:
            logger.info("Initializing in-memory mongomock database client...")
            self.client = mongomock.MongoClient()
            self.db = self.client[settings.DATABASE_NAME]
            self.is_connected = True
            self.is_mock = True
            self.init_indexes()
            return

        try:
            logger.info("Connecting to MongoDB at %s...", target_uri)
            # Short timeout so connection failure is detected immediately
            real_client = MongoClient(target_uri, serverSelectionTimeoutMS=2500)
            # Verify connectivity with server_info / ping
            real_client.admin.command("ping")
            self.client = real_client
            self.db = self.client[settings.DATABASE_NAME]
            self.is_connected = True
            self.is_mock = False
            logger.info("Successfully connected to real MongoDB: %s", settings.DATABASE_NAME)
            self.init_indexes()
        except Exception as exc:
            logger.warning(
                "Could not connect to MongoDB at %s: %s. Activating in-process resilient mock fallback.",
                target_uri,
                exc,
            )
            self.client = mongomock.MongoClient()
            self.db = self.client[settings.DATABASE_NAME]
            self.is_connected = True
            self.is_mock = True
            self.init_indexes()

    def disconnect(self) -> None:
        if self.client:
            try:
                self.client.close()
            except Exception as e:
                logger.error("Error closing MongoDB connection: %s", e)
            finally:
                self.client = None
                self.db = None
                self.is_connected = False
                self.is_mock = False
                logger.info("MongoDB connection closed.")

    def init_indexes(self) -> None:
        if self.db is None:
            return
        try:
            # Schemes indexes
            schemes_col = self.db["schemes"]
            schemes_col.create_index("id", unique=True)
            schemes_col.create_index("category")
            schemes_col.create_index("beneficiary_types")

            # Centers indexes
            centers_col = self.db["centers"]
            centers_col.create_index("id", unique=True)
            centers_col.create_index("district")
            centers_col.create_index("taluk")
            centers_col.create_index("center_type")

            # Users indexes
            users_col = self.db["users"]
            users_col.create_index("email", unique=True)
            users_col.create_index("id", unique=True)
            logger.info("Database indexes initialized successfully.")
        except Exception as exc:
            logger.warning("Index initialization note: %s", exc)

    def get_database(self) -> Database:
        if self.db is None:
            self.connect()
        return self.db  # type: ignore


db_manager = DatabaseManager()


def get_db() -> Database:
    return db_manager.get_database()
