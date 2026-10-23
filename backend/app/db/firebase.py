import logging
import os
from typing import Optional, Any, Dict, List
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client as FirestoreClient
from app.core.config import settings

logger = logging.getLogger("ruralconnect.db")


class MockDocumentSnapshot:
    def __init__(self, doc_id: str, data: Optional[Dict[str, Any]]):
        self.id = doc_id
        self._data = data

    @property
    def exists(self) -> bool:
        return self._data is not None

    def to_dict(self) -> Optional[Dict[str, Any]]:
        return dict(self._data) if self._data else None


class MockDocumentReference:
    def __init__(self, doc_id: str, collection_dict: Dict[str, Dict[str, Any]]):
        self.id = doc_id
        self._collection = collection_dict

    def get(self) -> MockDocumentSnapshot:
        data = self._collection.get(self.id)
        return MockDocumentSnapshot(self.id, data)

    def set(self, data: Dict[str, Any], merge: bool = False) -> None:
        if merge and self.id in self._collection:
            self._collection[self.id].update(data)
        else:
            self._collection[self.id] = dict(data)


class MockCollectionReference:
    def __init__(self, name: str, store: Dict[str, Dict[str, Dict[str, Any]]]):
        self.name = name
        self._store = store
        if name not in self._store:
            self._store[name] = {}
        self._items = self._store[name]
        self._filters: List[Any] = []
        self._limit: Optional[int] = None
        self._offset: int = 0

    def document(self, doc_id: str) -> MockDocumentReference:
        return MockDocumentReference(doc_id, self._items)

    def where(self, field: str, op: str, value: Any) -> "MockCollectionReference":
        clone = MockCollectionReference(self.name, self._store)
        clone._filters = list(self._filters)
        clone._filters.append((field, op, value))
        clone._limit = self._limit
        clone._offset = self._offset
        return clone

    def limit(self, count: int) -> "MockCollectionReference":
        clone = MockCollectionReference(self.name, self._store)
        clone._filters = list(self._filters)
        clone._limit = count
        clone._offset = self._offset
        return clone

    def offset(self, count: int) -> "MockCollectionReference":
        clone = MockCollectionReference(self.name, self._store)
        clone._filters = list(self._filters)
        clone._limit = self._limit
        clone._offset = count
        return clone

    def _matches(self, doc_data: Dict[str, Any]) -> bool:
        for field, op, val in self._filters:
            actual = doc_data.get(field)
            if op == "==" and actual != val:
                return False
            elif op == "array_contains" and (not isinstance(actual, list) or val not in actual):
                return False
        return True

    def stream(self):
        matched = []
        for doc_id, doc_data in self._items.items():
            if self._matches(doc_data):
                matched.append(MockDocumentSnapshot(doc_id, doc_data))
        
        if self._offset:
            matched = matched[self._offset:]
        if self._limit is not None:
            matched = matched[:self._limit]
        return matched

    def get(self):
        return list(self.stream())


class MockFirestoreClient:
    def __init__(self):
        self._store: Dict[str, Dict[str, Dict[str, Any]]] = {
            "schemes": {},
            "centers": {},
            "users": {},
        }
        self.project = "mock-ruralconnect-karnataka"

    def collection(self, name: str) -> MockCollectionReference:
        return MockCollectionReference(name, self._store)

    def close(self):
        pass


class DatabaseManager:
    client: Optional[Any] = None
    app: Optional[firebase_admin.App] = None
    is_connected: bool = False
    is_mock: bool = False

    def connect(self, force_mock: bool = False) -> None:
        if force_mock:
            logger.info("Initializing in-memory mock Firestore client...")
            self.client = MockFirestoreClient()
            self.is_connected = True
            self.is_mock = True
            return

        try:
            logger.info("Connecting to Firebase Cloud Firestore (Project: %s)...", settings.FIREBASE_PROJECT_ID)
            
            # Check if Firebase app already initialized
            existing_apps = firebase_admin._apps
            if "default" not in existing_apps and not firebase_admin._DEFAULT_APP_NAME in existing_apps:
                if settings.FIREBASE_CREDENTIALS_JSON and settings.FIREBASE_CREDENTIALS_JSON.strip():
                    import json
                    cred_dict = json.loads(settings.FIREBASE_CREDENTIALS_JSON)
                    cred = credentials.Certificate(cred_dict)
                    self.app = firebase_admin.initialize_app(cred, {"projectId": settings.FIREBASE_PROJECT_ID})
                elif settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                    self.app = firebase_admin.initialize_app(cred, {"projectId": settings.FIREBASE_PROJECT_ID})
                else:
                    # Uses Application Default Credentials (gcloud or GCP environment)
                    self.app = firebase_admin.initialize_app(options={"projectId": settings.FIREBASE_PROJECT_ID})
            else:
                self.app = firebase_admin.get_app()

            self.client = firestore.client(app=self.app)
            self.is_connected = True
            self.is_mock = False
            logger.info("Successfully connected to Firebase Firestore: %s", settings.FIREBASE_PROJECT_ID)
        except Exception as exc:
            logger.warning(
                "Could not connect to Firebase Firestore (%s): %s. Activating in-process resilient mock fallback.",
                settings.FIREBASE_PROJECT_ID,
                exc,
            )
            self.client = MockFirestoreClient()
            self.is_connected = True
            self.is_mock = True

    def disconnect(self) -> None:
        if self.client and hasattr(self.client, "close"):
            try:
                self.client.close()
            except Exception as e:
                logger.error("Error closing Firestore connection: %s", e)
        self.client = None
        self.is_connected = False
        self.is_mock = False
        logger.info("Firebase Firestore connection closed.")

    def get_database(self) -> Any:
        if self.client is None or not self.is_connected:
            self.connect()
        return self.client


db_manager = DatabaseManager()


def get_db() -> Any:
    return db_manager.get_database()
