from typing import Optional, Dict, Any
from app.db.firebase import get_db


class UserRepository:
    def _collection(self):
        return get_db().collection("users")

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        col = self._collection()
        normalized_email = email.lower().strip()
        query = col.where("email", "==", normalized_email).limit(1)
        docs = list(query.stream())
        if docs and docs[0].exists:
            data = docs[0].to_dict()
            if data and "id" not in data:
                data["id"] = docs[0].id
            return data
        return None

    def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        col = self._collection()
        doc = col.document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            if data and "id" not in data:
                data["id"] = doc.id
            return data
        
        query = col.where("id", "==", user_id).limit(1)
        docs = list(query.stream())
        if docs and docs[0].exists:
            data = docs[0].to_dict()
            if data and "id" not in data:
                data["id"] = docs[0].id
            return data
        return None

    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        col = self._collection()
        clean_user = dict(user_data)
        clean_user["email"] = clean_user["email"].lower().strip()
        doc_id = clean_user.get("id") or clean_user["email"]
        
        col.document(doc_id).set(clean_user)
        return clean_user
