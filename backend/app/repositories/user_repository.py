from typing import Optional, Dict, Any
from app.db.mongodb import get_db


class UserRepository:
    def _collection(self):
        return get_db()["users"]

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        col = self._collection()
        return col.find_one({"email": email.lower().strip()}, {"_id": 0})

    def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        col = self._collection()
        return col.find_one({"id": user_id}, {"_id": 0})

    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        col = self._collection()
        clean_user = dict(user_data)
        clean_user["email"] = clean_user["email"].lower().strip()
        col.insert_one(clean_user)
        # Return without MongoDB internal _id
        clean_user.pop("_id", None)
        return clean_user
