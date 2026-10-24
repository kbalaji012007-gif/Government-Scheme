from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.repositories.scheme_repository import SchemeRepository
from app.schemas.scheme import SchemeListResponse, SchemeSummary, SchemeDetail, DocumentRequirement

scheme_repo = SchemeRepository()


class SchemeService:
    def list_schemes(
        self,
        category: Optional[str] = None,
        beneficiary_type: Optional[str] = None,
        query: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> SchemeListResponse:
        page = max(1, page)
        page_size = max(1, min(50, page_size))

        raw_items, total = scheme_repo.find_schemes(
            category=category,
            beneficiary_type=beneficiary_type,
            query=query,
            page=page,
            page_size=page_size,
        )

        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        summaries = [SchemeSummary(**item) for item in raw_items]

        return SchemeListResponse(
            items=summaries,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def get_scheme_by_id(self, scheme_id: str) -> SchemeDetail:
        doc = scheme_repo.get_by_id(scheme_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scheme with ID '{scheme_id}' was not found",
            )
        return SchemeDetail(**doc)

    def get_scheme_documents(self, scheme_id: str) -> List[DocumentRequirement]:
        scheme = self.get_scheme_by_id(scheme_id)
        return scheme.required_documents
