from typing import Optional
from fastapi import HTTPException, status
from app.repositories.center_repository import CenterRepository
from app.schemas.center import CenterListResponse, CenterSummary, CenterDetail

center_repo = CenterRepository()


class CenterService:
    def list_centers(
        self,
        district: Optional[str] = None,
        taluk: Optional[str] = None,
        center_type: Optional[str] = None,
        query: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> CenterListResponse:
        page = max(1, page)
        page_size = max(1, min(50, page_size))

        raw_items, total = center_repo.find_centers(
            district=district,
            taluk=taluk,
            center_type=center_type,
            query=query,
            page=page,
            page_size=page_size,
        )

        filter_options = center_repo.get_filter_options()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        summaries = [CenterSummary(**item) for item in raw_items]

        return CenterListResponse(
            items=summaries,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            districts=filter_options["districts"],
            taluks=filter_options["taluks"],
            center_types=filter_options["center_types"],
        )

    def get_center_by_id(self, center_id: str) -> CenterDetail:
        doc = center_repo.get_by_id(center_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service center with ID '{center_id}' was not found",
            )
        return CenterDetail(**doc)
