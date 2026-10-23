import re
from typing import List, Optional, Tuple, Dict, Any
from app.db.firebase import get_db


class CenterRepository:
    def _collection(self):
        return get_db().collection("centers")

    def find_centers(
        self,
        district: Optional[str] = None,
        taluk: Optional[str] = None,
        center_type: Optional[str] = None,
        query: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List[Dict[str, Any]], int]:
        col = self._collection()
        docs_stream = col.stream()
        all_centers: List[Dict[str, Any]] = []

        for doc in docs_stream:
            data = doc.to_dict()
            if not data:
                continue
            if "id" not in data:
                data["id"] = doc.id
            all_centers.append(data)

        filtered = all_centers

        if district and district.lower() != "all":
            dist_lower = district.lower().strip()
            filtered = [c for c in filtered if str(c.get("district", "")).lower().strip() == dist_lower]

        if taluk and taluk.lower() != "all":
            taluk_lower = taluk.lower().strip()
            filtered = [c for c in filtered if str(c.get("taluk", "")).lower().strip() == taluk_lower]

        if center_type and center_type.lower() != "all":
            ctype_lower = center_type.lower().strip()
            filtered = [c for c in filtered if str(c.get("center_type", "")).lower().strip() == ctype_lower]

        if query and query.strip():
            q_lower = query.strip().lower()
            matched = []
            for c in filtered:
                name_en = str(c.get("name_en", "")).lower()
                name_kn = str(c.get("name_kn", "")).lower()
                addr_en = str(c.get("address_en", "")).lower()
                addr_kn = str(c.get("address_kn", "")).lower()
                dist = str(c.get("district", "")).lower()
                tal = str(c.get("taluk", "")).lower()

                if (
                    q_lower in name_en
                    or q_lower in name_kn
                    or q_lower in addr_en
                    or q_lower in addr_kn
                    or q_lower in dist
                    or q_lower in tal
                ):
                    matched.append(c)
            filtered = matched

        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        items = filtered[start:end]

        return items, total

    def get_by_id(self, center_id: str) -> Optional[Dict[str, Any]]:
        col = self._collection()
        doc = col.document(center_id).get()
        if doc.exists:
            data = doc.to_dict()
            if data and "id" not in data:
                data["id"] = doc.id
            return data
        
        query_docs = list(col.where("id", "==", center_id).limit(1).stream())
        if query_docs and query_docs[0].exists:
            data = query_docs[0].to_dict()
            if data and "id" not in data:
                data["id"] = query_docs[0].id
            return data
        return None

    def get_filter_options(self) -> Dict[str, List[str]]:
        col = self._collection()
        try:
            docs = col.stream()
            districts = set()
            taluks = set()
            center_types = set()

            for doc in docs:
                data = doc.to_dict()
                if data:
                    if data.get("district"):
                        districts.add(str(data["district"]))
                    if data.get("taluk"):
                        taluks.add(str(data["taluk"]))
                    if data.get("center_type"):
                        center_types.add(str(data["center_type"]))

            return {
                "districts": sorted(list(districts)),
                "taluks": sorted(list(taluks)),
                "center_types": sorted(list(center_types)),
            }
        except Exception:
            return {"districts": [], "taluks": [], "center_types": []}
