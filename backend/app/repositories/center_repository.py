import re
from typing import List, Optional, Tuple, Dict, Any
from app.db.mongodb import get_db


class CenterRepository:
    def _collection(self):
        return get_db()["centers"]

    def find_centers(
        self,
        district: Optional[str] = None,
        taluk: Optional[str] = None,
        center_type: Optional[str] = None,
        query: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List[Dict[str, Any]], int]:
        filter_dict: Dict[str, Any] = {}

        if district and district.lower() != "all":
            filter_dict["district"] = {"$regex": f"^{re.escape(district)}$", "$options": "i"}

        if taluk and taluk.lower() != "all":
            filter_dict["taluk"] = {"$regex": f"^{re.escape(taluk)}$", "$options": "i"}

        if center_type and center_type.lower() != "all":
            filter_dict["center_type"] = {"$regex": f"^{re.escape(center_type)}$", "$options": "i"}

        if query and query.strip():
            safe_query = re.escape(query.strip())
            regex_pat = {"$regex": safe_query, "$options": "i"}
            filter_dict["$or"] = [
                {"name_en": regex_pat},
                {"name_kn": regex_pat},
                {"address_en": regex_pat},
                {"address_kn": regex_pat},
                {"district": regex_pat},
                {"taluk": regex_pat},
            ]

        col = self._collection()
        total = col.count_documents(filter_dict)
        skip = (page - 1) * page_size

        cursor = col.find(filter_dict, {"_id": 0}).skip(skip).limit(page_size)
        items = list(cursor)
        return items, total

    def get_by_id(self, center_id: str) -> Optional[Dict[str, Any]]:
        col = self._collection()
        return col.find_one({"id": center_id}, {"_id": 0})

    def get_filter_options(self) -> Dict[str, List[str]]:
        col = self._collection()
        try:
            districts = sorted(list(set(col.distinct("district"))))
            taluks = sorted(list(set(col.distinct("taluk"))))
            center_types = sorted(list(set(col.distinct("center_type"))))
            return {
                "districts": [d for d in districts if d],
                "taluks": [t for t in taluks if t],
                "center_types": [c for c in center_types if c],
            }
        except Exception:
            return {"districts": [], "taluks": [], "center_types": []}
