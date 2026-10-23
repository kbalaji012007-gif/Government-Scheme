import re
from typing import List, Optional, Tuple, Dict, Any
from app.db.firebase import get_db


class SchemeRepository:
    def _collection(self):
        return get_db().collection("schemes")

    def find_schemes(
        self,
        category: Optional[str] = None,
        beneficiary_type: Optional[str] = None,
        query: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List[Dict[str, Any]], int]:
        col = self._collection()
        docs_stream = col.stream()
        all_schemes: List[Dict[str, Any]] = []

        for doc in docs_stream:
            data = doc.to_dict()
            if not data:
                continue
            if "id" not in data:
                data["id"] = doc.id
            all_schemes.append(data)

        filtered = all_schemes

        # Filter by category
        if category and category.lower() != "all":
            cat_lower = category.lower()
            filtered = [s for s in filtered if str(s.get("category", "")).lower() == cat_lower]

        # Filter by beneficiary_type
        if beneficiary_type and beneficiary_type.lower() != "all":
            ben_lower = beneficiary_type.lower()
            filtered = [
                s for s in filtered
                if any(str(b).lower() == ben_lower for b in s.get("beneficiary_types", []))
            ]

        # Filter by query search (bilingual support)
        if query and query.strip():
            q_lower = query.strip().lower()
            matched = []
            for s in filtered:
                name_en = str(s.get("name_en", "")).lower()
                name_kn = str(s.get("name_kn", "")).lower()
                short_en = str(s.get("short_description_en", "")).lower()
                short_kn = str(s.get("short_description_kn", "")).lower()
                tags = [str(t).lower() for t in s.get("tags", [])]

                if (
                    q_lower in name_en
                    or q_lower in name_kn
                    or q_lower in short_en
                    or q_lower in short_kn
                    or any(q_lower in t for t in tags)
                ):
                    matched.append(s)
            filtered = matched

        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        items = filtered[start:end]

        return items, total

    def get_by_id(self, scheme_id: str) -> Optional[Dict[str, Any]]:
        col = self._collection()
        doc = col.document(scheme_id).get()
        if doc.exists:
            data = doc.to_dict()
            if data and "id" not in data:
                data["id"] = doc.id
            return data
        
        # Fallback query if document key was auto-generated
        query_docs = list(col.where("id", "==", scheme_id).limit(1).stream())
        if query_docs and query_docs[0].exists:
            data = query_docs[0].to_dict()
            if data and "id" not in data:
                data["id"] = query_docs[0].id
            return data
        return None

    def count_by_category(self) -> Dict[str, int]:
        col = self._collection()
        docs = col.stream()
        categories = ["farmers", "students", "women", "senior_citizens", "rural_families", "general"]
        counts: Dict[str, int] = {cat: 0 for cat in categories}

        for doc in docs:
            data = doc.to_dict()
            if data:
                cat = str(data.get("category", "")).lower()
                if cat in counts:
                    counts[cat] += 1
        return counts
