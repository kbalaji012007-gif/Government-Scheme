import re
from typing import List, Optional, Tuple, Dict, Any
from app.db.mongodb import get_db


class SchemeRepository:
    def _collection(self):
        return get_db()["schemes"]

    def find_schemes(
        self,
        category: Optional[str] = None,
        beneficiary_type: Optional[str] = None,
        query: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List[Dict[str, Any]], int]:
        filter_dict: Dict[str, Any] = {}

        if category and category.lower() != "all":
            filter_dict["category"] = category.lower()

        if beneficiary_type and beneficiary_type.lower() != "all":
            filter_dict["beneficiary_types"] = beneficiary_type.lower()

        if query and query.strip():
            safe_query = re.escape(query.strip())
            regex_pat = {"$regex": safe_query, "$options": "i"}
            filter_dict["$or"] = [
                {"name_en": regex_pat},
                {"name_kn": regex_pat},
                {"short_description_en": regex_pat},
                {"short_description_kn": regex_pat},
                {"tags": regex_pat},
            ]

        col = self._collection()
        total = col.count_documents(filter_dict)
        skip = (page - 1) * page_size

        cursor = col.find(filter_dict, {"_id": 0}).skip(skip).limit(page_size)
        items = list(cursor)
        return items, total

    def get_by_id(self, scheme_id: str) -> Optional[Dict[str, Any]]:
        col = self._collection()
        doc = col.find_one({"id": scheme_id}, {"_id": 0})
        return doc

    def count_by_category(self) -> Dict[str, int]:
        col = self._collection()
        counts: Dict[str, int] = {}
        # Fetch distinct categories and count
        categories = ["farmers", "students", "women", "senior_citizens", "rural_families", "general"]
        for cat in categories:
            counts[cat] = col.count_documents({"category": cat})
        return counts
